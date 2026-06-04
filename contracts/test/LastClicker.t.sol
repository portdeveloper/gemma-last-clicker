// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "forge-std/Test.sol";
import "../src/LastClicker.sol";

// Human fix. Gemma's tests reverted on the first `click{value:}` because the
// players were never funded (no vm.deal) and it used precompile addresses
// (address(1)/(2)). It chased timing (vm.warp/vm.roll) for three rounds instead.
// Funding the accounts is the real fix, and it shows the contract was correct.
contract LastClickerTest is Test {
    LastClicker public game;
    address player1;
    address player2;

    function setUp() public {
        game = new LastClicker();
        player1 = makeAddr("player1");
        player2 = makeAddr("player2");
        vm.deal(player1, 1 ether);
        vm.deal(player2, 1 ether);
    }

    function test_ClickAccumulatesPotAndResetsTimer() public {
        uint256 initialTime = game.gameEndTime();
        vm.warp(block.timestamp + 1); // advance so the reset deadline is strictly later
        vm.prank(player1);
        game.click{value: 0.001 ether}();
        assertEq(game.pot(), 0.001 ether);
        assertGt(game.gameEndTime(), initialTime);
    }

    function test_OnlyLastClickerCanClaim() public {
        vm.prank(player1);
        game.click{value: 0.001 ether}();
        vm.prank(player2);
        game.click{value: 0.001 ether}();

        vm.warp(game.gameEndTime() + 1);

        vm.prank(player1);
        vm.expectRevert("You were not the last clicker");
        game.claim();

        vm.prank(player2);
        game.claim();
        assertEq(game.pot(), 0);
    }

    function test_GameEndsAfterClaim() public {
        vm.prank(player1);
        game.click{value: 0.001 ether}();

        vm.warp(game.gameEndTime() + 1);

        vm.prank(player1);
        game.claim();

        assertEq(game.gameActive(), false);

        vm.prank(player2);
        vm.expectRevert("Game is currently closed for claiming");
        game.click{value: 0.001 ether}();
    }
}
