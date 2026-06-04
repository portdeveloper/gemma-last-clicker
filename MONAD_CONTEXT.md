# Building on Monad: context for an LLM

Paste this into any model before you ask it to build on Monad. A model trained on Ethereum
and Solidity already knows ~95% of what it needs; this is the last 5%, plus the specific
things a local Gemma 4 12B got wrong in a real build (see ../failures.md, ../build-log).

## What Monad is, for build purposes
- An EVM L1 that runs EVM bytecode. Use standard tooling unchanged: Foundry, viem, wagmi, ethers.
  No special SDK, no separate language. If it compiles for Anvil, it works here.
- Fast: ~1s finality. Design frontends for it (don't assume ~12s blocks).

## Deploy (the entire chain-specific footprint)
- Testnet RPC: `https://testnet-rpc.monad.xyz`
- Chain id: **10143** (Foundry auto-detects it from the endpoint, so deploy is one URL):
  ```bash
  forge create src/YourContract.sol:YourContract \
    --rpc-url https://testnet-rpc.monad.xyz --private-key $PK --broadcast
  ```
- Native token: MON. Faucet (works for agents, no auth):
  ```bash
  curl -X POST https://agents.devnads.com/v1/faucet \
    -H "Content-Type: application/json" -d '{"chainId":10143,"address":"0x..."}'
  ```

## Frontend chain config (viem)
```js
import { defineChain } from 'https://esm.sh/viem@2'
export const monadTestnet = defineChain({
  id: 10143,
  name: 'Monad Testnet',
  nativeCurrency: { name: 'MON', symbol: 'MON', decimals: 18 },
  rpcUrls: { default: { http: ['https://testnet-rpc.monad.xyz'] } },
})
```
The RPC sends CORS headers, so browser reads via a public client work directly.
To switch wallets to it: `wallet_switchEthereumChain` with `chainId: '0x279f'` (hex of 10143).

## Things models get wrong (observed with Gemma 4 12B)
- It imported `"hardhat"` in a Foundry test. This is Foundry: tests use `import "forge-std/Test.sol"`,
  deploy in tests with `new YourContract()`.
- It hallucinated viem APIs: non-existent named imports (`publicAddress`, `solidityAbiInterpreter`),
  `contract.writeMethods.x.encoded`, a chain shaped as `rpcUrls.default.transport`, and
  `wallet_switchChain`. The real ones: `createPublicClient`/`createWalletClient` with a `transport`
  (`http()` / `custom(window.ethereum)`), `readContract`/`writeContract`, `rpcUrls.default.http: [url]`,
  `wallet_switchEthereumChain` with a hex chain id.
- Foundry tests must fund test accounts: `vm.deal(addr, 1 ether)` before any `click{value:}`,
  and use `makeAddr(...)` instead of `address(1)/(2)`.
- Don't use `block.timestamp` for adversarial randomness or tight timers; on a ~1s chain a
  validator can nudge it. forge's linter flags it.
- Use checks-effects-interactions for payouts (zero state before the external call). Gemma got
  this one right on its own.
