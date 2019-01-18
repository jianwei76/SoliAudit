const Web3 = require("web3");
const RLP = require('rlp');  

/*
if (typeof web3 !== 'undefined') {
    web3 = new Web3(web3.currentProvider);
} else {
    // set the provider you want from Web3.providers
    web3 = new Web3(new Web3.providers.HttpProvider(RPC_URI));
}
*/

for (var i = 0; i < 256; i++){
    var hash = "0x" + Web3.utils.sha3(RLP.encode([i]));
    consloe.log(hash);
}
