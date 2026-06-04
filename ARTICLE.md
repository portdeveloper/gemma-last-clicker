<!-- DRAFT in port's voice, from the REAL run (build-log/, failures.md). Framing is
     transparent: a frontier model (Claude) drove a local Gemma. Adjust the framing, the
     opener, and the verdict to taste. Frontmatter shape from the puddleswap post.
     Run it past STYLE.md once more before publishing. -->

<!-- title options (sentence case, lowercase i):
     - i let a free model on my laptop build a dapp. it dodged the famous bug and tripped on the basics
     - a free 12B wrote a safe contract, then couldn't fix its own tests
     - i pointed claude at a free local model and told it to build a monad dapp -->

---
title: "[TK: pick a title]"
description: "I had a frontier model drive a free local Gemma 4 12B to build a dapp. It wrote a safe contract, couldn't fix its own tests, and never knew it was on Monad."
slug: "[TK: e.g. free-local-model-built-my-dapp]"
published_at: "[TK: 2026-06-XXT12:00:00Z]"
modified_at: "[TK: 2026-06-XXT12:00:00Z]"
date_display: "[TK: June XX, 2026]"
section: "Developer tools"
tags:
  - Gemma
  - Monad
  - AI
keywords:
  - gemma 4
  - monad
  - local llm
  - dapp
  - foundry
cover:
  src: "assets/articles/[TK-slug]/cover.svg"
  alt: "[TK: cover alt]"
  og_alt: "[TK]"
originally_published:
  platform: X
  url: "https://x.com/port_dev"
---

![cover [TK]](assets/articles/[TK-slug]/cover.svg)

A free model that fits on a laptop wrote me a reentrancy-safe Solidity contract, and then spent three rounds failing to fix a test bug it could see in its own output.

I work at Monad, so the question I actually wanted answered was whether a free, open model you run yourself is good enough to build a real dapp for an EVM chain. So I had Claude drive a local Gemma 4 12B over its API, gave it a game to build, and never told the model what chain it would end up on. I just watched what came out and fixed it where it got stuck.

## The setup

Gemma 4 12B dropped on June 3rd. The thing that caught my eye wasn't a score, it was the license: Apache 2.0 now, so you can run it, fine-tune it, and ship it with no strings. It fits in about 16GB. I ran it locally with llama.cpp on Metal, no API key, nothing leaving the machine, somewhere around 20-40 tokens a second.

The driver was a small script: Claude prompts Gemma, writes whatever code comes back into a Foundry project, runs `forge build` or `forge test`, and pastes the error back. That loop, over and over. The game is last-clicker: a pot, a short timer, every click is a transaction, and the last person to click before the clock hits zero takes the pot. The whole build ran against Anvil, Foundry's local node, so there was no chain to name yet.

## What it got right

The game logic was right on the first try. Fee per click, pot accumulates, timer resets, only the last clicker can claim, game closes after a payout.

And the part I expected it to fail, it nailed. The payout zeroes the pot before it sends, and uses `.transfer()`. That's checks-effects-interactions, the pattern that stops a reentrancy attack. I had money on it writing the naive version, the exact shape of the bug that drained the DAO in 2016 and split Ethereum in two. It didn't. A free 12B on my laptop quietly avoided the most famous footgun in the language. (`.transfer()` is the dated way to be safe, but it is safe.) Credit where it's due, then.

## Where it broke

It could not hand me a project that compiled. The first version had a Hardhat import in a Foundry test, two `constructor()` functions in one contract, a modifier that was actually a function, and a made-up `deploy()` call in the test. None of it builds.

Here's the surprising part: I pasted back only the first compiler error, the Hardhat import, and it fixed everything in one shot. Merged the constructors, replaced the bogus modifier with a real `require`, rewrote the test against `forge-std`. One round, all of it, gone. For a free local model that is genuinely good.

Then it hit a wall it never got over. The tests compiled but every one reverted on the first `click`, because the test never funded the player accounts. The fix is one line, `vm.deal`. I fed it the failure three times. Three times it added `vm.warp` and `vm.roll`, chasing a timing theory, and three times the tests failed byte for byte, same gas to the digit. It could write the code. It could not debug the code, even with the error sitting in front of it. I funded the accounts myself and all three passed, which also proved the contract had been right the whole time.

The frontend told the same story louder. I asked for a single-file page with viem, and it produced a genuinely nice UI, glass cards, a live countdown, the works. The web3 layer underneath was fiction: imports that don't exist in viem, a contract object with methods I've never seen, the wrong wallet RPC call. I stopped feeding it errors and rewrote the seventy lines of viem myself, because that's exactly the kind of specific-library detail a small model makes up. The UI was its work. The wiring was mine.

So here's the lesson: **a free local model writes plausible code fast, especially the well-worn stuff, and falls apart on two things, the exact API of a specific library and debugging a failure it can already see.** It's a fast junior who can't yet read a stack trace.

## The reveal: it was Monad, and it took one line

I never told the model what chain this was for, because there was nothing to tell. Anvil is just the EVM on my machine, and everything it wrote was plain EVM code. When the contract and tests were green, I pointed Foundry at one URL:

```bash
forge create src/LastClicker.sol:LastClicker --rpc-url https://testnet-rpc.monad.xyz --broadcast
```

Foundry read the chain id off the endpoint by itself. It deployed first try. The chain was Monad, and the model never knew, because it never needed to: Monad runs EVM bytecode, so the Solidity it already knew was already correct. The only Monad-specific fact in the whole build was a single RPC URL. Even the testnet MON came from an agent faucet over an API call, so no human funded it either.

One honest asterisk forge's linter flagged: the timer leans on `block.timestamp`, which validators can nudge. That matters more on a chain with one-second blocks than on one with twelve, and it's the kind of thing you'd tighten before mainnet.

## Play it

It's live on Monad testnet: [TK: https://gemma-last-clicker.vercel.app]. Connect a wallet, grab testnet MON, and click. Every click is a real transaction confirmed in about a second for a fraction of a cent, which is the only reason a last-second game like this works on-chain at all. [TK: drop the clip of rapid clicks here.]

So, can a free model on your laptop build a real dapp? [TK: your honest verdict. Mine, as a draft: it gets you a safe, working contract and a pretty frontend, and then a human spends an hour fixing the tests and the wiring it couldn't. That's further than I expected, and not yet far enough to leave alone.]

The repo, every prompt, and the full build log are here: [TK: repo link]. The one file that taught any model to deploy to Monad correctly is [TK: MONAD_CONTEXT.md link]. Go build something.
