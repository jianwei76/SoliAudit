const rlp = require('rlp');
const keccak = require('keccak');
const RandExp = require('randexp');

const generate = require('ethjs-account').generate;

for (var g = 0; g < 100000000; g++) {
    var re = /.{64}/;
    input = new RandExp(re).gen();
    console.log(g,'-----');

    var ans = generate(input);

    for (var i = 0; i <=10; i++) {

        //var i = 217;
        var nonce = '0x' + i.toString(16); //The nonce must be a hex literal!

        var sender = ans.address; //Requires a hex string as input!

        var input_arr = [sender, nonce];
        var rlp_encoded = rlp.encode(input_arr);

        var contract_address_long = keccak('keccak256').update(rlp_encoded).digest('hex');

        var contract_address = contract_address_long.substring(24); //Trim the first 24 characters.

        if (contract_address.indexOf('badc0de') > 0) {
            console.log('!!!!!!!!!!!nonce:', nonce, ", contract_address: " + contract_address);
            console.log('ans:', ans);
            process.exit(1);
        }

    }
}


