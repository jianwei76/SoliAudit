pragma solidity ^0.4.21;

contract HoneyPot {
    mapping (address => uint) public balances;
   
    function HoneyPot() payable {
        put();
    }

     
    function put() payable {
        balances[msg.sender] = msg.value;
    }

    function get() {

        if (!msg.sender.call.value(balances[msg.sender])()) {
            throw;
        }
        balances[msg.sender] = 0;
    }
    
    function test(uint8 num) returns (uint8 _underflow) { 
	   uint8 xx = num +5 ;	
	   return xx;
    }

    function() {
        throw;
    }
}


