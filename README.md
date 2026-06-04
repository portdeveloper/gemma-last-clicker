# last-clicker (built by Gemma 4 12B, driven by Claude)

A "last clicker" game on Monad testnet: last click before the timer ends wins the pot.
Every click is a transaction.

The contract was written by **Gemma 4 12B** (free, open, run locally via llama.cpp on Metal),
driven by Claude over the model's local API. The honest build log is the point of the repo,
see `ARTICLE.md`, `failures.md`, and `build-log/`.

- **Live demo:** https://gemma-last-clicker.vercel.app
- **Contract** (Monad testnet, chain 10143): `0x0507d7290992B475ED3FC83AF9d54aa8A29D4005`
  (verified: [monadscan](https://testnet.monadscan.com/address/0x0507d7290992B475ED3FC83AF9d54aa8A29D4005) · [monadvision](https://testnet.monadvision.com/address/0x0507d7290992B475ED3FC83AF9d54aa8A29D4005))
- **Frontend:** `frontend/index.html` (Gemma wrote the UI; the viem layer was hallucinated and rewritten by hand)

## contracts (Foundry)
```bash
cd contracts
forge build
forge test     # 3/3 pass
```
`src/LastClicker.sol` (Gemma), `test/LastClicker.t.sol` (Gemma's tests, funding fixed by hand).

## deploy to monad testnet (the entire chain-specific footprint)
```bash
forge create src/LastClicker.sol:LastClicker \
  --rpc-url https://testnet-rpc.monad.xyz --private-key $PK --broadcast
```
Chain id is auto-detected (10143). Testnet MON came from the agent faucet:
`POST https://agents.devnads.com/v1/faucet {"chainId":10143,"address":"0x..."}`.

## run the model loop yourself
`build-log/drive.py` and `build-log/drive-tests.py` drive Gemma through the compile and test
loops against a running llama.cpp server (`../run-model.sh`).

## license
MIT
