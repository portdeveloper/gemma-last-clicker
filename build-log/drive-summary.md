# Drive summary - COMPILES

## round1-build (Gemma's original) - exit 1

```
Unable to resolve imports:
      "hardhat" in "/Users/port/repos/experiments/gemma-web3/contracts/test/LastClicker.t.sol"
with remappings:
      forge-std/=/Users/port/repos/experiments/gemma-web3/contracts/lib/forge-std/src/
Compiling 2 files with Solc 0.8.30
Solc 0.8.30 finished in 45.11ms
Error: Compiler run failed:
Error (6275): Source "hardhat" not found: File not found. Searched the following locations: "/Users/port/repos/experiments/gemma-web3/contracts".
ParserError: Source "hardhat" not found: File not found. Searched the following locations: "/Users/port/repos/experiments/gemma-web3/contracts".
 --> test/LastClicker.t.sol:4:1:
  |
4 | import "hardhat"; // If using standard, but for Foundry we use:
  | ^^^^^^^^^^^^^^^^^
```

## round2-build (wrote ['src', 'test']) - OK

```
Compiling 21 files with Solc 0.8.30
Solc 0.8.30 finished in 423.64ms
Compiler run successful!
warning[block-timestamp]: usage of `block.timestamp` in a comparison may be manipulated by validators
   ╭▸ contracts/src/LastClicker.sol:35:17
   │
35 │         require(block.timestamp >= gameEndTime, "Timer has not expired yet");
   │                 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   │
   ╰ help: https://book.getfoundry.sh/reference/forge/forge-lint#block-timestamp

warning[block-timestamp]: usage of `block.timestamp` in a comparison may be manipulated by validators
   ╭▸ contracts/src/LastClicker.sol:57:13
   │
57 │         if (block.timestamp >= gameEndTime) return 0;
   │             ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   │
   ╰ help: https://book.getfoundry.sh/reference/forge/forge-lint#block-timestamp
```

