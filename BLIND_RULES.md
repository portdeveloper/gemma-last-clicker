# Blind build — ground rules

The experiment: can a free, local 12B model (Gemma 4 12B via llama.cpp on Metal) build a real web3
dapp from scratch? Keep it honest, keep it logged. The article is only as good as the log.

## What Gemma gets
- Its own knowledge of Solidity, EVM, Foundry, viem/wagmi.
- A local Anvil RPC to build and test against.
- The task (build a last-clicker pot dapp).

## What Gemma does NOT get
- The target chain. It is not told it's building for Monad. The build is chain-agnostic.
- Any chain docs during the build.

## Blind mode: pure model, escalate when stuck
- Run Gemma 4 12B with llama.cpp's server on Metal (local, free, no API), prompt it in the
  browser chat at http://127.0.0.1:8080 (restart with ./run-model.sh). It's a chat UI, so
  you're the hands: copy its output into the project, run it, paste errors back. Thinking is
  on by default; if a reply is empty, raise the token limit. Logging stays trivial.
- Prompt Gemma from its own knowledge. You paste code into the project, run
  `forge build` / `forge test` / the frontend, and feed errors back as prompts.
- Escalation rule: if it's stuck after ~2-3 iterations on the same error, hand it a minimal
  doc snippet or search result. Log every escalation in `failures.md` (what it was stuck on,
  what you gave it, did it unblock).

## Deploy
- The ONLY Monad-specific input in the whole build is the RPC: `https://testnet-rpc.monad.xyz`
- Chain ID is auto-detected by Foundry from the endpoint. No docs dump, keep context clean.
- The frontend needs the chain id + native symbol; derive them from the same RPC, don't hardcode.

## Logging discipline
- Every prompt, verbatim -> `prompts.md`.
- Every failure -> `failures.md`. Note who fixed each (Gemma or you).
- Don't silently fix the model's mistakes. Log them first, then fix.
- Don't fake the reentrancy beat. If the model writes safe code, record that as the finding.

## Recording (key moments only)
- Screen-record: the first contract attempt, the reentrancy discovery, the frontend coming
  together, and the final last-second-click demo on testnet.
- Everything else lives in the markdown logs.
