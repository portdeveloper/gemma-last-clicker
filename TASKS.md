# Tasks split

The article is a true account, so the experiment is yours and the writing is mine. Run
yours, I do mine in parallel, we assemble at the seam.

## YOUR TASKS (only you + Gemma can do these)
1. [ ] Get Gemma 4 12B running in Unsloth Studio; install Foundry + Anvil. Confirm with a test prompt.
2. [ ] Run the blind build (see BLIND_RULES.md). Gemma writes the last-clicker contract.
       Log every prompt -> prompts.md, every failure -> failures.md.
3. [ ] Capture Gemma's FIRST payout/claim function verbatim, before you fix anything (the centerpiece).
4. [ ] Get it compiling + tested on Anvil. Note every fix and who made it (Gemma or you).
5. [ ] Gemma builds the viem/wagmi frontend; keep logging.
6. [ ] Deploy to Monad testnet: faucet for MON, point forge at https://testnet-rpc.monad.xyz, deploy.
       Write down EXACTLY what changed from Anvil (this is the reveal).
7. [ ] Verify the contract on the explorer.
8. [ ] Host the frontend on Vercel; make it playable. Decide the RPC for it.
9. [ ] Screen-record the key moments + the last-second-click clip.
10. [ ] Hand back: prompts.md, failures.md, final contract + frontend, deployed address, live URL,
        the clip, and a 2-line "what surprised me good / bad".
11. [ ] (last) Publish under your byline; post the thread.

## MY TASKS (true regardless of the run; no fabrication)
1. [x] ARTICLE.md draft in your voice: connective prose written, your run-data as [TK] slots.
2. [x] MONAD_CONTEXT.md baseline (EVM-compatible, standard tooling, one-RPC deploy, no block
       randomness, checks-effects-interactions), with slots for the gaps Gemma actually hit.
3. [x] README skeleton for the repo.
4. [x] THREAD.md skeleton (structure + slots for the real punch + clip).
5. [ ] BLOCKED ON YOUR RUN: after you hand me the contract, write the reentrancy PoC + Foundry
       tests proving the exploit and the fix, and help with the deploy.
6. [ ] BLOCKED ON YOUR RUN: assemble the final article from your logs, gut-check against STYLE.md.

## The seam
You fill the [TK] slots in ARTICLE.md from prompts.md / failures.md. I turn that into the
finished piece. Nothing in ARTICLE.md claims what Gemma did until you fill those slots.
