var Transaction = require('ethereumjs-tx');

// var tx1 = 
//     { nonce: 0,
//     gasPrice: '0x3b9aca00',
//     gasLimit: '0x5208',
//     to: '0x92b28647ae1f3264661f72fb2eb9625a89d88a31',
//     value: '0x1111d67bb1bb0000',
//     data: '0x',
//     v: 41,
//     r: '0x69a726edfb4b802cbf267d5fd1dabcea39d3d7b4bf62b9eeaeba387606167166',
//     s: '0x7724cedeb923f374bef4e05c97426a918123cc4fec7b07903839f12517e1b3c8' 
// }
// let t1 = new Transaction(tx1);
// console.log(t1.hash(true).toString("hex"));



    var z1 = 0x061bf0b4b5fdb64ac475795e9bc5a3978f985919ce6747ce2cfbbcaccaf51009;
    var s1 = 0x2bbd9c2a6285c2b43e728b17bda36a81653dd5f4612a2e0aefdb48043c5108de;
    var r = 0x69a726edfb4b802cbf267d5fd1dabcea39d3d7b4bf62b9eeaeba387606167166;
    var z2 = 0xd79fc80e7b787802602f3317b7fe67765c14a7d40c3e0dcb266e63657f881396;
    var s2 = 0x7724cedeb923f374bef4e05c97426a918123cc4fec7b07903839f12517e1b3c8; 
    var key =((z1*s2 - z2*s1)/(r*(s1-s2)));    
    console.log(key);