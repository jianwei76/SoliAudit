const RandExp = require('randexp');
var rando = require('random-number-in-range');
const Web3 = require('web3');
const _ = require('underscore');
var accountlist;
let web3 = new Web3();
var first = false;
var second = false;
var third = false;
var gasPricev = 100000;
var temp_inputtype = {};
var count =0;
function fuzzinput(account) {

    accountlist = account;
    first = true;
    second = true;
    third = true;
    temp_inputtype = {};
    count=0;
    gasPricev = 100000;
}



fuzzinput.prototype.generate = function generate(obj) {
	//console.log('==============,count',count++);
    var input_type = obj.args;
    var stateMutability = obj.stateMutability;
    var function_name = obj.name;
    if (!input_type) {
        throw new Error('must provide input args');
    }

    var inputs = [];
    count++;
    let r = Math.floor(Math.random() * accountlist.length)
    var random_account = accountlist[r];
 	//var random_account = accountlist[ count % 3];
 	//console.log('random_account=',r);
    //check first time and second time fuzz - for fuzz min and max value
    if (!_.isEqual(temp_inputtype, input_type)) {
        first = true;
        second = true;
        third = true;

    } else {
        if (first == true) {
            first = false;
        } else if (second == true) {
            second = false;
        } else {
            third = false;
        }
    }

    for (var i = 0; i < input_type.length; i++) {

        //console.log(input_type[i].name,'-------',input_type[i].type);

        let input = '';

        var type = input_type[i].type;
         var arg_name = input_type[i].name;
        if (type == 'address') {
            input = accountlist[Math.floor(Math.random() * accountlist.length)];
        } else if (type.startsWith('uint') == true) {

                bits = type.slice(4);
                input = toFixed(rando(1, Math.pow(2, parseInt(bits))));
               //input = web3.toWei(rando(1, 2), 'ether')
            
        } else if (type.startsWith('address[]') == true) {
            input = accountlist.slice(0, (Math.floor(Math.random() * accountlist.length)));
        } else if (type == 'string') {

            if (function_name.endsWith('_underflow') && arg_name.startsWith('extreme_flow')) {
                input = '0';
            } else if (function_name.endsWith('_overflow') && arg_name.startsWith('extreme_flow')) {
                input = 'Max value';
            } else {
                var re = /.+/;
                input = new RandExp(re).gen();
            }
        } else if (type == 'bool') {
            input = (Math.random() >= 0.5) ? 'True' : 'False';
        }


        inputs.push(input);
    }

    temp_inputtype = input_type;

    var random_value = web3.toWei(rando(1, 2), 'ether') ;
    var transaction_object;
    //console.log(stateMutability);
    gasPricev = gasPricev-10;
    //console.log('ether',gasPricev);
    if (stateMutability == 'payable') {
        transaction_object = { from: random_account ,gas: 1000000 ,gasPrice: web3.toWei(gasPricev, 'gwei'), value: random_value };
    } else {
        transaction_object = { from: random_account ,gas: 1000000 ,gasPrice: web3.toWei(gasPricev, 'gwei') };
    }



    inputs.push(transaction_object);
    return (inputs);
}


function scientificToDecimal(num) {
    //if the number is in scientific notation remove it
    if (/\d+\.?\d*e[\+\-]*\d+/i.test(num)) {
        var zero = '0',
            parts = String(num).toLowerCase().split('e'), //split into coeff and exponent
            e = parts.pop(), //store the exponential part
            l = Math.abs(e), //get the number of zeros
            sign = e / l,
            coeff_array = parts[0].split('.');
        if (sign === -1) {
            num = zero + '.' + new Array(l).join(zero) + coeff_array.join('');
        } else {
            var dec = coeff_array[1];
            if (dec) l = l - dec.length;
            num = coeff_array.join('') + new Array(l + 1).join(zero);
        }
    }

    return num;
}


function toFixed(x) {
    if (Math.abs(x) < 1.0) {
        var e = parseInt(x.toString().split('e-')[1]);
        if (e) {
            x *= Math.pow(10, e - 1);
            x = '0.' + (new Array(e)).join('0') + x.toString().substring(2);
        }
    } else {
        var e = parseInt(x.toString().split('+')[1]);
        if (e > 20) {
            e -= 20;
            x /= Math.pow(10, e);
            x += (new Array(e + 1)).join('0');
        }
    }
    return parseFloat(x);
}


module.exports = fuzzinput;