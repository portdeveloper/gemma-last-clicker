# X thread (draft)

Same shape as the article: hook -> the model -> the build -> the bug -> the one-line reveal
-> play it. Fill [TK] from the real run. One idea per post, no thread-filler.

1/ [TK: the real result in one line. e.g. "i gave a free 12B model running on my laptop a
   dapp to build, and never told it what chain it would run on. it shipped."]

2/ the model: gemma 4 12b. apache 2.0 now, so no license strings. runs in ~16gb in unsloth
   studio. free, local, no api key, nothing leaves the laptop.

3/ the build: pure model, its own knowledge, against a local anvil node. i was the hands,
   it wrote the code. every prompt is logged: [TK: repo link]

4/ what it got right: [TK: the good surprise, one line + a screenshot]

5/ where it broke: [TK: the headline failure, one line + a screenshot]

6/ the one that matters: [TK: the payout. if it wrote a reentrancy bug, this is the post.
   "a free model on my laptop reached for the exact bug that drained the DAO in 2016." show
   the diff, the fix is moving one line.]

7/ the reveal: it was monad. the only chain-specific thing in the entire build was one RPC
   url. evm bytecode in, evm bytecode out, the model never knew the difference. [TK: the
   change-list, ideally "that was it"]

8/ play it: [TK: live url] + a clip of rapid last-second clicks. every click is a real tx,
   confirmed in ~1s. that's the only reason a last-second game works on-chain.

9/ repo + a context file that makes any model build on monad correctly: [TK: links]
