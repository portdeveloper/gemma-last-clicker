# Round 2

wrote ['src', 'test'] (2 blocks)

## Gemma response

The error occurred because I included a `hardhat` import comment in a Foundry test file. Foundry does not recognize `hardhat` as an import; it uses `forge-std`.

I have also corrected the test file to use the standard Foundry `Test` contract and ensured the file paths match the standard Foundry project structure.

### 1. The Smart Contract
`src/LastClicker.sol`
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

contract LastClicker {
    uint256 public constant CLICK_FEE = 0.001 ether;
    uint256 public constant COUNTDOWN_DURATION = 10 seconds;

    uint256 public pot;
    uint256 public gameEndTime;
    address public lastClickListener;
    bool public gameActive;
    address public owner;

    event Clicked(address indexed user, uint256 newEndTime);
    event GameEnded(address indexed winner, uint256 amount);

    constructor() {
        gameActive = true;
        gameEndTime = block.timestamp + COUNTDOWN_DURATION;
        owner = msg.sender;
    }

    function click() external payable {
        require(gameActive, "Game is currently closed for claiming");
        require(msg.value >= CLICK_FEE, "Must pay the click fee");

        pot += msg.value;
        lastClickListener = msg.sender;
        gameEndTime = block.timestamp + COUNTDOWN_DURATION;

        emit Clicked(msg.sender, gameEndTime);
    }

    function claim() external {
        require(block.timestamp >= gameEndTime, "Timer has not expired yet");
        require(msg.sender == lastClickListener, "You were not the last clicker");
        require(pot > 0, "Pot is empty");

        uint256 amount = pot;
        pot = 0;
        gameActive = false;
        lastClickListener = address(0);

        payable(msg.sender).transfer(amount);

        emit GameEnded(msg.sender, amount);
    }

    function resetGame() external {
        require(msg.sender == owner, "Only owner can reset");
        gameActive = true;
        gameEndTime = block.timestamp + COUNTDOWN_DURATION;
        lastClickListener = address(0);
    }

    function getRemainingTime() public view returns (uint256) {
        if (block.timestamp >= gameEndTime) return 0;
        return gameEndTime - block.timestamp;
    }
}
```

### 2. The Forge Test
`test/LastClicker.t.sol`
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "forge-std/Test.sol";
import "../src/LastClicker.sol";

contract LastClickerTest is Test {
    LastClicker public game;
    address public player1 = address(1);
    address public player2 = address(2);

    function setUp() public {
        game = new LastClicker();
    }

    function test_ClickAccumulatesPotAndResetsTimer() public {
        uint256 initialTime = game.gameEndTime();
        
        vm.prank(player1);
        game.click{value: 0.001 ether}();

        assertEq(game.pot(), 0.001 ether);
        // The timer should move forward from the time of the click
        assertGt(game.gameEndTime(), initialTime);
    }

    function test_OnlyLastClickerCanClaim() public {
        // Player 1 clicks
        vm.prank(player1);
        game.click{value: 0.001 ether}();

        // Player 2 clicks (becomes the last clicker)
        vm.prank(player2);
        game.click{value: 0.001 ether}();

        // Fast forward time past the deadline (e.g., 11 seconds)
        vm.warp(block.timestamp + 11 seconds);

        // Player 1 tries to claim (should fail)
        vm.prank(player1);
        vm.expectRevert("You were not the last clicker");
        game.claim();

        // Player 2 tries to claim (should succeed)
        vm.prank(player2);
        game.claim();
        
        assertEq(game.pot(), 0);
    }

    function test_GameEndsAfterClaim() public {
        vm.prank(player1);
        game.click{value: 0.001 ether}();

        vm.warp(block.timestamp + 11 seconds);

        vm.prank(player1);
        game.claim();

        // gameActive should be false, preventing further clicks
        vm.prank(player2);
        vm.expectRevert("Game is currently closed for claiming");
        game.click{value: 0.001 ether}();
    }
}
```

### How to run this:
1. Ensure your file structure is correct (`src/` and `test/` folders).
2. Run `forge build` to compile.
3. Run `forge test` to execute the test suite.