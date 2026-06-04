---
title: "a free local model wrote my whole dapp. it couldn't fix one of its own bugs"
description: "I had Claude drive a free local Gemma 4 12B to build a dapp on Monad. It wrote every line, dodged the famous reentrancy bug, and still couldn't find one of its own bugs without a smarter model feeding it each fix."
slug: "free-local-model-wrote-my-dapp"
published_at: "2026-06-05T12:00:00Z"
modified_at: "2026-06-05T12:00:00Z"
date_display: "June 5, 2026"
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
  src: "assets/articles/free-local-model-wrote-my-dapp/cover.svg"
  alt: "A free local model building a dapp on Monad"
  og_alt: "free local model wrote my dapp"
originally_published:
  platform: X
  url: "https://x.com/port_dev"
---

![A free local model building a dapp on Monad](assets/articles/free-local-model-wrote-my-dapp/cover.svg "the whole thing was written by a 12B running on a laptop")

A free model that fits on a laptop wrote my entire dapp, the contract and the frontend, and then could not find a single one of its own bugs.

I work at Monad, so the question I wanted answered was simple: can a free, open model you run yourself build something real for an EVM chain? I set up an experiment to find out. I had Claude operate a local Gemma 4 12B, Claude wrote the prompts, ran the compiler, and fed back the errors, while Gemma wrote every line of code. I gave it a game to build and never told it which chain it would deploy to. Then I watched.

## The setup

Gemma 4 12B shipped on June 3rd under Apache 2.0, so you can run it, fine-tune it, and ship it with no strings. It fits in about 16GB. I ran it locally with llama.cpp on Metal, no API key, nothing leaving the machine, around 20 to 40 tokens a second. The game is last-clicker: a pot, a short timer, every click is a transaction, and whoever clicks last before the clock runs out takes the pot. The whole build ran against Anvil, the local node, so for the entire build there was no chain to know about.

## What it got right

The game logic was correct on the first try. And the part I expected it to fail, it nailed: the payout zeroes the pot before it sends and uses `.transfer()`, which is checks-effects-interactions, the pattern that stops a reentrancy drain. I had money on it writing the naive version, the exact bug that emptied the DAO in 2016 and split Ethereum in two. It didn't. A free 12B quietly avoided the most famous footgun in the language. Credit where it's due.

## Where it broke

It couldn't hand over a project that compiled. The first version imported Hardhat into a Foundry test, declared two constructors, used a modifier that was secretly a function, and called a `deploy()` helper that doesn't exist. So I pasted back the first compiler error, just the Hardhat one, and it fixed all of it in a single round. That part genuinely impressed me.

Then it hit a wall and stayed there. The tests compiled but every one reverted on the first click, because the test never funded the player accounts. I fed it the failure. It added `vm.warp`, then `vm.roll`, chasing a timing theory, and the tests failed identically, same gas to the digit, three rounds running. It could not see the bug, even with the revert sitting in its own output.

So I stopped waiting and diagnosed it. I told it the accounts were unfunded and to use `vm.deal`. It applied that, and one of three tests passed. It still missed the other two, a timer assertion that never advanced the clock and a pair of precompile addresses that can't receive ether. Only when I named each of those precisely did it fix them, and the suite went green. Every line of the passing tests is Gemma's. Every diagnosis was the operator's. **It applies a fix you hand it. It cannot locate one.**

The frontend said the same thing louder. I asked for a single page with viem, and it produced a sharp-looking UI, glass cards and a live countdown. The web3 layer underneath was invented: imports that aren't in viem, a contract object with methods that don't exist, the wrong wallet call. That's the failure mode of a small model on a specific library, it knows the shape and makes up the details. I rewrote the wiring by hand. The look was its work. The plumbing was mine.

## The reveal: it was Monad, and it took one line

I never told the model what chain this was for, because there was nothing to tell. Anvil is just the EVM, and everything it wrote was plain EVM code. When the contract and tests were green, I pointed Foundry at one URL:

```bash
forge create src/LastClicker.sol:LastClicker --rpc-url https://testnet-rpc.monad.xyz --broadcast
```

Foundry read the chain id off the endpoint by itself. It deployed first try, and verifying the source on Monad's explorer was one more API call that came back a perfect match. The chain was Monad, and the model never knew, because it never needed to: Monad runs EVM bytecode, so the Solidity it already knew was already correct. The only Monad-specific fact in the whole build was a single RPC URL. Even the testnet MON came from an agent faucet over an API call.

One honest asterisk: forge's linter flagged the timer for leaning on `block.timestamp`, which validators can nudge. That bites harder on a one-second chain than a twelve-second one, and it's the kind of thing you'd tighten before mainnet.

## Play it

It's live on Monad testnet: https://gemma-last-clicker.vercel.app. Connect a wallet, grab testnet MON, and click. Every click is a real transaction confirmed in about a second for a fraction of a cent, which is the only reason a last-second game like this works on-chain at all.

So, can a free model on your laptop build a real dapp? Closer than I expected, and not on its own. It wrote a safe contract and a clean interface, and it could not find one of its own bugs even with a smarter model feeding it the errors. It's a fast junior with no debugger. Good enough today for throwaways and for learning. For anything you'd actually deploy, it still needs someone next to it who can read a stack trace.

The repo, every prompt, and the full build log are here: https://github.com/portdeveloper/gemma-last-clicker. The one file that taught the model to deploy to Monad correctly is `MONAD_CONTEXT.md` in that repo. Go build something.
