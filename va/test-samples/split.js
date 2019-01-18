        
var receive1 = "0x1660f7fe64d738e2a86b439aedd818b010521e93";
var receive2 = "0x5fc1b18f0b3131ffa66a9b5755bfa1dbc677742e";

var splitetherContract = web3.eth.contract([{"inputs":[{"name":"receive1","type":"address"},{"name":"receive2","type":"address"}],"payable":true,"stateMutability":"payable","type":"constructor"}]);
var splitether = splitetherContract.new(
   receive1,
   receive2,
   {
     from: web3.eth.accounts[0], 
     data: '0x606060405260405160408060f38339810160405280805190602001909190805190602001909190505060008273ffffffffffffffffffffffffffffffffffffffff166108fc600234811515604f57fe5b049081150290604051600060405180830381858888f1935050505090508173ffffffffffffffffffffffffffffffffffffffff166108fc600234811515609157fe5b049081150290604051600060405180830381858888f19350505050905050505060358060be6000396000f3006060604052600080fd00a165627a7a72305820321050249e5d78a4b13af4ea651c39ad9164076c3deb5cb9c6f1eaa2ceba5ca20029', 
     gas: '4700000'
   }, function (e, contract){
    console.log(e, contract);
    if (typeof contract.address !== 'undefined') {
         console.log('Contract mined! address: ' + contract.address + ' transactionHash: ' + contract.transactionHash);
    }
 })
