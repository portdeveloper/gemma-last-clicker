# Round 7 (dictated the timer warp + makeAddr fixes)

## response

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "forge-std/Test.sol";
import "../src/LastClicker.sol";

contract LastClickerTest is Test {
    LastClicker public game;
    address public player1;
    address public player2;
    uint256 constant FUND = 1 ether;

    function setUp() public {
        // Use makeAddr to avoid using precompile addresses (address(1), address(2))
        player1 = makeAddr("p1");
        player2 = makeAddr("p2");

        // Fund players so they can actually perform the click action
        vm.deal(player1, FUND);
        vm.deal(player2, FUND);
        
        game = new LastClicker();
    }

    function test_ClickAccumulatesPotAndResetsTimer() public {
        // Advance time slightly before the first action to ensure there is a baseline
        vm.warp(block.timestamp + 1);
        
        uint256 initialTime = game.gameEndTime();
        
        vm.prank(player1);
        game.click{value: 0.001 ether}();

        assertEq(game.pot(), 0.001 ether);
        // Verify the end time actually moved forward from the original timestamp
        assertGt(game.gameEndTime(), initialTime);
    }

    function test_OnlyLastClickerCanClaim() public {
        // Player 1 clicks
        vm.prank(player1);
        game.click{value: 0.001 ether}();

        // Player 2 clicks
        vm.prank(player2);
        game.click{value: 0.001 ether}();

        uint256 deadline = game.gameEndTime();

        // Jump time 1 second past the deadline
        vm.warp(deadline + 1);
        // Ensure the block number increments to avoid timestamp/block issues
        vm.roll(1);

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
        // Player 1 clicks
        vm.prank(player1);
        game.click{value: 0.001 ether}();

        // Jump time to past the deadline
        vm.warp(game.gameEndTime() + 1);
        vm.roll(1);

        // Player 1 claims
        vm.prank(player1);
        game.claim();

        // Verify gameActive is false
        assertEq(game.gameActive(), false);

        // Try to click again (should fail because gameActive is false)
        vm.prank(player2);
        vm.expectRevert("Game is currently closed for claiming");
        game.click{value: 0.001 ether}();
    }
}
```