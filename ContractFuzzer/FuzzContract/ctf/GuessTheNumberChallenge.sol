pragma solidity ^0.4.8;

contract GuessTheNumberChallenge {
    uint8 answer = 0;

    function GuessTheNumberChallenge() public payable {
        require(msg.value == 1 ether);
    }

    function isComplete() public view returns (bool) {
        return address(this).balance == 0;
    }

    function guess(uint8 n) public payable {
        require(msg.value == 1 ether);

        if (n == answer) {
            msg.sender.call.value(address(this).balance)();
        }
    }
}


