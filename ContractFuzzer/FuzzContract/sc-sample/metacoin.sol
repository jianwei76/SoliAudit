pragma solidity ^0.4.2;

contract MetaCoin {
	mapping (address => uint) balances;

	function MetaCoin() 
	{
		balances[tx.origin] = 10000;
	}
	event Transfer(address indexed _from, address indexed _to, uint256 _value);

	function sendCoin(address receiver, uint amount)  returns(bool sufficient) {
		
		if (balances[msg.sender] < amount) 
		{
			Transfer(msg.sender, receiver, amount);
			//require(balances[msg.sender] > amount) ;
			 //revert();
			//Transfer(msg.sender, receiver, amount);
		}
		
	
		balances[msg.sender] -= amount;
		balances[receiver] += amount;
		Transfer(msg.sender, receiver, amount);

	}

	function getBalance(address addr) constant  returns(uint) 
	{	

		return balances[addr];

	}
}