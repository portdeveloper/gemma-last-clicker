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
