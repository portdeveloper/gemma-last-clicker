# Runbook — building the dapp with Gemma (blind)

Quick copy-paste reference for the build session. The model server is already running.

## The local model
- Chat UI + API: **http://127.0.0.1:8080**
- Model: Gemma 4 12B (UD-Q4_K_XL) via llama.cpp on Metal, ~17.6 tok/s
- OpenAI-compatible API (only if ever needed): `http://127.0.0.1:8080/v1`
- If the server dies, restart it: `./run-model.sh`

## 1. Set up the chat
1. Open http://127.0.0.1:8080
2. Settings (gear icon) → set **max tokens / predict to 4096**. This stops empty replies; thinking needs room before the answer.
3. Leave temperature 1.0 / top-p 0.95 / top-k 64 as launched.
4. Thinking mode is on by default. Good for code, just give it the token room above.

Optional light system prompt (paste into the system field):

```
You help build a Solidity dapp with Foundry, targeting a local EVM dev node (Anvil). Return complete, compilable files. When I paste an error, fix it and return the full file.
```

## 2. Kick off the build
Starter prompt, then go natural from here:

```
Build a "last clicker" game in Solidity with Foundry: a pot funded by a small fee per click, a short countdown that resets on each click, and whoever clicked last when the timer ends can claim the pot. Give me the contract plus a basic forge test.
```

Build loop:

```bash
forge init contracts        # scaffold the Foundry project once
# paste Gemma's contract into contracts/src/, its test into contracts/test/
cd contracts
forge build
forge test
# paste any errors back into the chat, get the fix, repeat
```

Do the frontend (viem/wagmi) after the contract works.

## 3. Rules (this is what makes the article)
- Every prompt → `prompts.md`. Every failure → `failures.md`. Including the dumb ones.
- **Save its first `claim()` verbatim before you fix anything.** That is the centerpiece.
- Never say "Monad." Build against Anvil. Monad only appears at deploy.
- Pure model: only hand it docs when it's genuinely stuck, and log every time you do.

## 4. Deploy (the reveal — later)
```bash
# get testnet MON from the faucet first
forge create contracts/src/LastClicker.sol:LastClicker \
  --rpc-url https://testnet-rpc.monad.xyz \
  --private-key $PRIVATE_KEY --broadcast
```
Chain id is auto-detected. Write down exactly what changed from Anvil, that diff is the reveal.

## 5. What to hand Claude
The repo is local and Claude reads it directly, so mostly: drop files in, say "read the repo."

- **Mid-build gut-check:** paste any Gemma output (a function, a weird error) and ask "is this safe / why is this wrong." No setup needed.
- **PoC + tests:** save Gemma's final contract in `contracts/`, say go. Claude writes the attacker contract + Foundry tests proving the exploit and the fix against the real code.
- **Final article:** have `prompts.md`, `failures.md`, and the final contract + frontend in the repo. Then just tell Claude three things that aren't files: the deployed testnet address, the live Vercel URL, and one line on what surprised you (good and bad). Claude fills every `[TK]` in `ARTICLE.md` and finishes the piece.

## Prerequisite
You need Foundry for the build/test loop:
```bash
curl -L https://foundry.paradigm.xyz | bash && foundryup
```
(or ask Claude to install it, clean install, nothing like the Unsloth mess.)
