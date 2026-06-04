"""Drive Gemma 4 12B through a compile-fix loop for the last-clicker contract.
Prompt -> write code -> forge build -> feed the error back -> repeat. Thinking off
for speed on the fix rounds. Logs every round to build-log/. Honest record of the
real exchanges; nothing here is hand-edited."""
import json, re, os, subprocess, urllib.request

HOME = os.path.expanduser("~")
PROJ = HOME + "/repos/experiments/gemma-web3"
DIR  = PROJ + "/contracts"
LOG  = PROJ + "/build-log"
ENDPOINT = "http://127.0.0.1:8080/v1/chat/completions"
FORGE = HOME + "/.foundry/bin/forge"
os.makedirs(LOG, exist_ok=True)

def call(messages, max_tokens=3500):
    body = json.dumps({"messages": messages, "max_tokens": max_tokens,
        "temperature": 1.0, "top_p": 0.95, "top_k": 64,
        "chat_template_kwargs": {"enable_thinking": False}}).encode()
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

def build():
    p = subprocess.run([FORGE, "build", "--root", DIR], capture_output=True, text=True)
    return p.returncode, (p.stdout + p.stderr)

first = json.load(open("/tmp/gemma-demo.json"))["choices"][0]["message"].get("content") or ""
SYS = ("You help build a Solidity dapp with Foundry (not Hardhat), targeting a local EVM dev "
       "node (Anvil). Return complete, compilable files in ```solidity code blocks.")
USER1 = ('Build a "last clicker" game in Solidity with Foundry: a pot funded by a small fee per '
         'click, a short countdown that resets on each click, and whoever clicked last when the '
         'timer ends can claim the pot. Give me the contract and a forge test.')
messages = [{"role": "system", "content": SYS},
            {"role": "user", "content": USER1},
            {"role": "assistant", "content": first}]

rc, out = build()
log = [("round1-build (Gemma's original)", rc, out)]
final = "DID NOT COMPILE"
for rnd in range(2, 8):
    if rc == 0:
        final = "COMPILES"; break
    messages.append({"role": "user", "content":
        "`forge build` failed. Fix all errors and return the complete corrected file(s) in code blocks. Compiler output:\n\n" + out[:4000]})
    try:
        resp = call(messages)
    except Exception as e:
        log.append((f"round{rnd}-ERROR", -1, repr(e))); break
    messages.append({"role": "assistant", "content": resp})
    wrote, n = write_blocks(resp)
    open(f"{LOG}/round{rnd}.md", "w").write(f"# Round {rnd}\n\nwrote {wrote} ({n} blocks)\n\n## Gemma response\n\n{resp}")
    rc, out = build()
    log.append((f"round{rnd}-build (wrote {wrote})", rc, out))

with open(f"{LOG}/drive-summary.md", "w") as f:
    f.write(f"# Drive summary - {final}\n\n")
    for name, code, o in log:
        f.write(f"## {name} - {'OK' if code == 0 else f'exit {code}'}\n\n```\n{o[-1200:].strip()}\n```\n\n")
json.dump(messages, open(f"{LOG}/transcript.json", "w"), indent=1)
print("FINAL:", final, "after", len(log), "builds")
