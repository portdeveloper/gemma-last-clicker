# PLAN — the blind build (Gemma 4 12B builds a last-clicker dapp, deployed to Monad)

Living execution plan. Design doc (full rationale):
`~/.gstack/projects/gemma-web3/port-unknown-design-20260604-170232.md`
Article voice: portdeveloper.github.io STYLE.md (puddleswap is the reference post).

## What we're making
A free local model (Gemma 4 12B via llama.cpp on Metal) builds a last-clicker pot dapp from scratch
against Foundry/Anvil. You deploy it untouched to Monad testnet, host a live Vercel demo,
and write an honest "what worked / what failed" report. Spine of the article is the
reentrancy beat (the model's first payout function is the DAO-hack shape). Monad is named
at the deploy beat, with the arc front-loaded per STYLE.md.

Ships: article + open repo + exact prompts + live demo URL + MONAD_CONTEXT.md.

## Decision log
- Dapp: last-clicker pot. Every click is a tx; a short timer leans on Monad's ~1s finality.
- Failure centerpiece: reentrancy in the payout (CEI / guard / pull-payment as the fix).
- Structure: front-loaded arc; chain name withheld one beat, not the outcome.
- Gemma's role: coding copilot, run blind to the chain. Not embedded in the dapp.
- Blind mode: PURE MODEL, escalate to docs/search only when genuinely stuck, log each escalation.
- Capture: markdown logs throughout + screen-record key moments and the final demo.
- Deploy input: hand the model ONLY the RPC `https://testnet-rpc.monad.xyz` (chain ID
  auto-detected by Foundry). No docs dump, keep context clean. Blind build + deploy-time
  reveal preserved. Proof line: "the only Monad-specific thing in the whole build was one URL."
- Episode 2 (not now): fine-tune Gemma on Monad docs via Unsloth, re-run, measure the delta.

## Owner tags
[you] — only you can do it · [you + Gemma] — the experiment, I stay hands-off the building ·
[you + me] — I can do the heavy lifting.

## Phase 0 — setup & facts  [you + me] · CAN START NOW
- [x] Gemma 4 12B facts (confirmed 2026-06-04; re-check primary sources before publish):
      released 2026-06-03; ~12B params; Apache 2.0 (fully permissive, unlike prior Gemma's
      restrictive license); 256K context; multimodal (text/image/video/audio); runs in 16GB
      VRAM or unified memory (4-bit ~8GB); runs locally via llama.cpp on Mac/Metal
      (unsloth/gemma-4-12b-it-GGUF, we run UD-Q4_K_XL at ~17.6 tok/s). Unsloth fine-tune
      (episode 2) needs a CUDA GPU, not this Mac.
- [ ] Monad testnet — the model gets ONLY the RPC `https://testnet-rpc.monad.xyz` at deploy
      (chain ID auto-detected from the endpoint). Record chain ID / explorer / faucet / TPS
      figures separately as our ground truth + for the article, not fed to the model. (you)
- [x] Gemma 4 12B running locally via llama.cpp on Metal (server at http://127.0.0.1:8080,
      ~17.6 tok/s; restart with ./run-model.sh). Unsloth Studio doesn't install on Apple Silicon.
- [ ] Confirm Foundry + Anvil installed and working. (you)
- [ ] Capture harness: prompt-log + failure-log templates, and the written blind ground
      rules (what context Gemma gets, the escalation rule). (me to draft, you to run)
Done when: facts confirmed in the doc, environment runs, harness templates exist.

## Phase 1 — the blind build on Anvil  [you + Gemma] · the article's substance
Protocol (pure model, escalate when stuck):
- Prompt Gemma in Unsloth from its own knowledge. You paste code into the project, run
  `forge build` / `forge test` / the frontend, and feed errors back as prompts.
- Escalation rule: if it's stuck after ~2-3 iterations on the same error, hand it the
  relevant doc snippet. Log the escalation (timestamp, what it was stuck on, what you gave
  it, did it unblock).
- Log every prompt verbatim, every failure, every fix and who made it (Gemma vs you).
- Screen-record the key moments: first contract attempt, the reentrancy discovery, the
  frontend coming together.

Steps:
- [ ] Gemma scaffolds the last-clicker contract (pot, short timer, click extends + sets leader).
- [ ] Capture the naive claim function (the reentrancy). Do not fix it silently — log it.
- [ ] Foundry tests green on Anvil (happy path + the timer/claim logic).
- [ ] Reentrancy beat: confirm the exploit with an attacker PoC; then fix (CEI + guard or
      pull-payment). (I can write the PoC and sanity-check the fix.)
- [ ] Gemma builds the viem/wagmi frontend (connect, click, live countdown, pot display).
- [ ] Log timer/finality assumptions (polling that assumes ~12s blocks, timestamp deadlines).
Done when: it works end-to-end on Anvil and the failure log is complete and honest.

## Phase 2 — deploy to Monad testnet  [you + me] · the reveal beat
- [ ] Get testnet MON from the faucet.
- [ ] Point Foundry at `https://testnet-rpc.monad.xyz` (chain ID auto-detected) and deploy.
      The only Monad-specific input in the whole build is this one URL. Frontend needs the
      chain id + native symbol too; derive them from the same RPC, don't hardcode.
- [ ] Verify the contract on Monad's explorer.
- [ ] Record EXACTLY what changed Anvil -> Monad. That diff is the EVM-equivalence proof.
- [ ] Smoke-test on testnet; note any non-1:1 gotchas (gas, timestamp/finality behavior).
Done when: the fixed contract is live + verified on Monad testnet and the change-list is captured.

## Phase 3 — live demo on Vercel  [you + me]
- [ ] Decide the Monad RPC for the frontend (public vs keyed).
- [ ] Point the frontend at Monad testnet; deploy to Vercel; make it playable; add a faucet link.
- [ ] Deploy the FIXED contract publicly. Keep the naive version + PoC in the repo, labeled.
- [ ] Record the last-second-click clip (the throughput payoff).
Done when: anyone can open the URL and play, and you have the clip.

## Phase 4 — MONAD_CONTEXT.md  [you + me]
- [ ] Distill the deploy diff + gotchas into a drop-in context file ("what a model needs to
      know to build on Monad"). This is the reusable takeaway and a standalone CTA.
Done when: a stranger could paste it into any model and get Monad-correct output.

## Phase 5 — write the article  [you + me]
- [ ] Draft in voice from the design-doc outline; front-loaded arc; reentrancy as the spine.
- [ ] Exact prompts as an appendix / inline call-outs.
- [ ] Gut-check against STYLE.md and the puddleswap voice. Frontmatter copied from an existing post.
Done when: it reads like you, the reveal lands as insight, and the verdict is honest.

## Phase 6 — ship & distribute  [you]
- [ ] Publish repo (MIT) with README linking the live demo + article.
- [ ] Publish the article.
- [ ] X thread re-cutting the arc + the clip, timed to the Gemma 4 conversation.
- [ ] Promote MONAD_CONTEXT.md on its own.

## Dependencies
0 -> 1 -> 2 -> 3; then 2 and 3 feed 4; everything feeds 5; 5 gates 6.
Phase 0 facts start now; the hardware check runs in parallel.

## Open decisions (resolve as you go)
- Timer length (short enough to need fast finality, long enough to be playable).
- Fix to feature: checks-effects-interactions, a reentrancy guard, or pull-payment.
- Include the attacker PoC in the repo? (Recommended: yes, labeled.)
- Seed a testnet pot for the demo, or fund purely by click fees.
- RPC provider for the Vercel app.
- Article home + byline; disclosure line wording.

## Risks (from design)
- Bait-and-switch reflex: front-load the arc, disclose Monad affiliation, name the chain at deploy.
- Exploitable public demo: ship the fixed contract; keep naive + PoC labeled in repo.
- Flaky RPC on the live demo is a bad first impression.
- Over-claiming the model; the failures are the credibility.
- Overlap with the existing vibe-code post; hold the differentiator (small/open/local + blind deploy).
