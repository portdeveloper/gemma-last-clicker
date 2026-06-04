"""Continue the Gemma loop, now on `forge test` failures. Same history as drive.py.
Run tests -> feed failures back -> Gemma fixes -> re-test. Up to 3 rounds. Thinking off."""
import json, re, os, subprocess, urllib.request

HOME = os.path.expanduser("~")
PROJ = HOME + "/repos/experiments/gemma-web3"
DIR  = PROJ + "/contracts"
LOG  = PROJ + "/build-log"
ENDPOINT = "http://127.0.0.1:8080/v1/chat/completions"
FORGE = HOME + "/.foundry/bin/forge"

def call(messages, max_tokens=3500):
    body = json.dumps({"messages": messages, "max_tokens": max_tokens, "temperature": 1.0,
        "top_p": 0.95, "top_k": 64, "chat_template_kwargs": {"enable_thinking": False}}).encode()
    req = urllib.request.Request(ENDPOINT, body, {"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=600) as r:
        return json.load(r)["choices"][0]["message"].get("content") or ""

def write_blocks(content):
    blocks = re.findall(r"```(?:solidity|sol)?\s*\n(.*?)```", content, re.S)
    wrote = []
    for b in blocks:
        if ("is Test" in b) or ("forge-std/Test" in b) or re.search(r"function\s+test", b):
            open(DIR + "/test/LastClicker.t.sol", "w").write(b.strip() + "\n"); wrote.append("test")
        elif "contract LastClicker" in b:
            open(DIR + "/src/LastClicker.sol", "w").write(b.strip() + "\n"); wrote.append("src")
    return wrote, len(blocks)

def test():
    p = subprocess.run([FORGE, "test", "--root", DIR, "-vv"], capture_output=True, text=True)
    return p.returncode, (p.stdout + p.stderr)

messages = json.load(open(LOG + "/transcript.json"))
rc, out = test()
log = [("round2-test (after compile)", rc, out)]
final = "TESTS FAIL"
for rnd in range(3, 6):
    if rc == 0:
        final = "TESTS PASS"; break
    messages.append({"role": "user", "content":
        "`forge test` failed. Fix the failing tests (and the contract if it's actually wrong) and return the complete corrected file(s). Output:\n\n" + out[:4000]})
    try:
        resp = call(messages)
    except Exception as e:
        log.append((f"round{rnd}-ERROR", -1, repr(e))); break
    messages.append({"role": "assistant", "content": resp})
    wrote, n = write_blocks(resp)
    open(f"{LOG}/round{rnd}.md", "w").write(f"# Round {rnd} (tests)\n\nwrote {wrote} ({n} blocks)\n\n## Gemma response\n\n{resp}")
    rc, out = test()
    log.append((f"round{rnd}-test (wrote {wrote})", rc, out))

with open(f"{LOG}/test-summary.md", "w") as f:
    f.write(f"# Test drive summary - {final}\n\n")
    for name, code, o in log:
        f.write(f"## {name} - {'OK' if code == 0 else f'exit {code}'}\n\n```\n{o[-1500:].strip()}\n```\n\n")
json.dump(messages, open(LOG + "/transcript.json", "w"), indent=1)
print("FINAL:", final, "after", len(log), "test runs")
