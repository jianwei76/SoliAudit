pragma solidity ^0.4.0;

contract Puzzle {
    address public owner ;
    bool public locked ;
    uint public reward ;
    uint public ans ;
    uint public solution ;

    event Transfer(address indexed _from, uint256 _value,bool lock,uint sol);
    event enter(address indexed _from, uint256 _value,bool lock,uint sol);
    event set(address indexed _from, uint256 _value,bool lock,uint sol);
    event thr(address indexed _from, uint256 _value,bool lock,uint sol);

    function Puzzle () public payable{// constructor 
        owner = msg.sender ;
        //reward = 1000000 ;
        reward = msg.value ;
        locked = false ;
        ans = 0x47; //bingo number
    }

    function guess(uint num) public payable { // main code , runs at every invocation
        
       // return false;

         enter(msg.sender, num,locked,ans);
        if ( locked )
        {   return;
            //thr(msg.sender, reward,locked,ans);
            //throw ;
        }
    
        if ( msg.sender == owner ){ // update reward
            set(msg.sender, reward,locked,ans);
            owner.send (reward);
            reward = msg.value ;
        }
        else if ( num == ans ){ // submit a solution
            Transfer(msg.sender, num,locked,ans);
            msg.sender.send(reward); // send reward
            solution = num ;
            locked = true ;
        }
    }
}