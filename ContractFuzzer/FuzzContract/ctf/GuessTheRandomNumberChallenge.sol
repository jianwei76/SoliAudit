pragma solidity ^0.4.4;

contract GuessTheRandomNumberChallenge {
    uint8 answer;

    
    function GuessTheRandomNumberChallenge()  payable {
        require(msg.value == 1 ether);
        bytes32 blocknum = 0xefdf45089c598a79f38780b19423a561e4b3207316af4b95d25f7d6119428001;
        uint timestamp = 1534148254;
        answer = uint8(keccak256(blocknum,timestamp));
    
    }

    function isComplete() public view returns (bool) {
        return address(this).balance == 0;
    }

    function guess(uint8 n) public payable {
        require(msg.value == 1 ether);

        if (n == answer) {
            //msg.sender.transfer(2 ether);
            msg.sender.call.value(address(this).balance)();
        }
    }

    
}