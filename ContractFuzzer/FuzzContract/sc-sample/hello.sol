pragma solidity ^0.4.21;


contract hello {

  //say hello mshk.top
  function say() public  returns (string) {
  	print('aa');
    return "Hello mshk.top";
  }

  //print name
  function print(string name) public  returns (string) {
  		//print(name);
    return name;
  }
}