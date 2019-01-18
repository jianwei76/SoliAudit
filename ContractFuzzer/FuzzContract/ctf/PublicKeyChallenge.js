var e = require('ethereumjs-util');
var Transaction = require('ethereumjs-tx');

var rawTx = {
    nonce: '0x00',
    gasPrice: '0x3b9aca00',
    gasLimit: '0x15f90',
    to: '0x6B477781b0e68031109f21887e6B5afEAaEB002b',
    value: '0x00',
    data: '0x5468616e6b732c206d616e21',
    v: '0x29',
    r: '0xa5522718c0f95dde27f0827f55de836342ceda594d20458523dd71a539d52ad7',
    s: '0x5710e64311d481764b5ae8ca691b05d14054782c7d489f3511a7abf2f5078962'
};


// var rawTx = 
// {
//   gasLimit: '0x5208',
//   gasPrice: '0x3b9aca00',
//   nonce: '0x00',
//   r: '0x69a726edfb4b802cbf267d5fd1dabcea39d3d7b4bf62b9eeaeba387606167166',
//   s: "0x7724cedeb923f374bef4e05c97426a918123cc4fec7b07903839f12517e1b3c8",
//   to: "0x92b28647ae1f3264661f72fb2eb9625a89d88a31",
//   v: '0x29',
//   data: '0x',
//   value: "1230000000000000000"
// }

var tx2= 
{
  gasLimit: '0x5208',
  gasPrice: "0x3b9aca00",
  nonce: '0x01',
  r: "0x69a726edfb4b802cbf267d5fd1dabcea39d3d7b4bf62b9eeaeba387606167166",
  s: "0x2bbd9c2a6285c2b43e728b17bda36a81653dd5f4612a2e0aefdb48043c5108de",
  to: "0x92b28647ae1f3264661f72fb2eb9625a89d88a31",
  v: "0x29",
  data: '0x',
  value: "1811266580600000000"
}




var tx = new Transaction(rawTx);
//console.log(e.bufferToHex(tx.getSenderPublicKey()).toString());


// var tx = new Transaction(tx2);
// console.log(e.bufferToHex(tx.getSenderPublicKey()).toString());

function toHex(str) {
 var hex = ''
 for(var i=0;i<str.length;i++) {
  hex += ''+str.charCodeAt(i).toString(16)
 }
 return hex
}




var EthUtil = require('ethereumjs-util')
var EthTx = require('ethereumjs-tx')



// signed tx
var signedTx = "0xf86b80843b9aca008252089492b28647ae1f3264661f72fb2eb9625a89d88a31881111d67bb1bb00008029a069a726edfb4b802cbf267d5fd1dabcea39d3d7b4bf62b9eeaeba387606167166a07724cedeb923f374bef4e05c97426a918123cc4fec7b07903839f12517e1b3c8"
// Create a tx object from signed tx 
var tx = new EthTx(signedTx)
console.log(EthUtil.bufferToHex(tx.hash(false)));

// Get an address of sender
var address = EthUtil.bufferToHex(tx.getSenderAddress())
// get a public key of sender
var publicKey = EthUtil.bufferToHex(tx.getSenderPublicKey())
// console.log(address)
// console.log(publicKey)

signedTx = "0xf86b01843b9aca008252089492b28647ae1f3264661f72fb2eb9625a89d88a31881922e95bca330e008029a069a726edfb4b802cbf267d5fd1dabcea39d3d7b4bf62b9eeaeba387606167166a02bbd9c2a6285c2b43e728b17bda36a81653dd5f4612a2e0aefdb48043c5108de"
// Create a tx object from signed tx 
tx = new EthTx(signedTx)

console.log(EthUtil.bufferToHex(tx.hash(false)));

// Get an address of sender
address = EthUtil.bufferToHex(tx.getSenderAddress())
// get a public key of sender

publicKey = EthUtil.bufferToHex(tx.getSenderPublicKey())
// console.log(address)
// console.log(publicKey)

