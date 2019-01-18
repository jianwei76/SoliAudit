var Transaction = require('ethereumjs-tx');



var EC = require('elliptic').ec;
var BN = require('bn.js');
var ec = new EC('secp256k1');
const keccak = require('keccak');
var G = ec.g; // Generator point
var pk = new BN('1'); // private key as big number
var pubPoint=G.mul(pk); // EC multiplication to determine public point 


var x = pubPoint.getX().toBuffer(); //32 bit x co-ordinate of public point 
var y = pubPoint.getY().toBuffer(); //32 bit y co-ordinate of public point 

var publicKey =Buffer.concat([x,y])
	
publicKey = Buffer.from('6bce79b40f2f2fb2c719ce0232a1de599f3fce410b4292d6bf6ac3570df98b1ee5e1ee8d0bab3d18ed6d87181bcce76c900cb9cb50e6dcfb8622fcfc98ba105f','hex');
const address =  keccak('keccak256').update(publicKey).digest()// keccak256 hash of  publicKey
console.log(address);
const buf2 = Buffer.from(address, 'hex');
console.log(buf2);
console.log("Ethereum Adress:::"+"0x"+buf2.slice(-20).toString('hex'))


var tx1 = 
    { nonce: 0,
    gasPrice: '0x3b9aca00',
    gasLimit: '0x5208',
    to: '0x92b28647ae1f3264661f72fb2eb9625a89d88a31',
    value: '0x1111d67bb1bb0000',
    data: '0x',
    v: 41,
    r: '0x69a726edfb4b802cbf267d5fd1dabcea39d3d7b4bf62b9eeaeba387606167166',
    s: '0x7724cedeb923f374bef4e05c97426a918123cc4fec7b07903839f12517e1b3c8' 
}
let t1 = new Transaction(tx1);
console.log(t1.hash(false).toString("hex"));



var tx2= {

  "gas": 21000,
  "gasPrice": "1000000000",
  "nonce": 1,
  "r": "0x69a726edfb4b802cbf267d5fd1dabcea39d3d7b4bf62b9eeaeba387606167166",
  "s": "0x2bbd9c2a6285c2b43e728b17bda36a81653dd5f4612a2e0aefdb48043c5108de",
  "to": "0x92b28647ae1f3264661f72fb2eb9625a89d88a31",
  "v": "0x29",
  "value": "1811266580600000000"
}
  
let t2 = new Transaction(tx2);
console.log(t2.hash(false).toString("hex"));


// var z1 = Buffer.from('061bf0b4b5fdb64ac475795e9bc5a3978f985919ce6747ce2cfbbcaccaf51009','hex');
 
// var s1 = Buffer.from('2bbd9c2a6285c2b43e728b17bda36a81653dd5f4612a2e0aefdb48043c5108de','hex');
 
// var r = Buffer.from('69a726edfb4b802cbf267d5fd1dabcea39d3d7b4bf62b9eeaeba387606167166','hex');

// var z2 = Buffer.from('d79fc80e7b787802602f3317b7fe67765c14a7d40c3e0dcb266e63657f881396','hex');

// var s2 = Buffer.from('7724cedeb923f374bef4e05c97426a918123cc4fec7b07903839f12517e1b3c8','hex');

//  //console.log(z1.toString('hex'));

//     // var z1 = 0x061bf0b4b5fdb64ac475795e9bc5a3978f985919ce6747ce2cfbbcaccaf51009;
//     // var s1 = 0x2bbd9c2a6285c2b43e728b17bda36a81653dd5f4612a2e0aefdb48043c5108de;
//     // var r = 0x69a726edfb4b802cbf267d5fd1dabcea39d3d7b4bf62b9eeaeba387606167166;
//     // var z2 = 0xd79fc80e7b787802602f3317b7fe67765c14a7d40c3e0dcb266e63657f881396;
//     // var s2 = 0x7724cedeb923f374bef4e05c97426a918123cc4fec7b07903839f12517e1b3c8; 
//     // var key =((z1*s2 - z2*s1)/(r*(s1-s2)));  

//     // console.log(key.toString('hex'));

// var a = 36694632194835572968265431002247246783319336123477273356976855818836060927464;
// var b = 80344699208465047886874733345656362080342753200335864009556811149836987934584;
// var c = 70488217795581073514279416920146171716125825384670304548754161399500291087556;
// var d = (b-a)/c;
// console.log(b-a);
// console.log(d);

 