pragma solidity^0.4.0;

contract ReentSend{
    uint public saved;

    function ReentSend() public payable{
        saved = msg.value;
    }

    function withdraw(uint key) public payable{
        //msg.sender.send(saved);
        msg.sender.call.value(saved)();
        saved = 0;
    }
}
