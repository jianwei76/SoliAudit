const Web3 = require("web3");
const RLP = require('rlp');  
const fs = require('fs');  
const sleep = require('sleep');

const LIMIT = 10;
const RPC_URI = "http://localhost:8545";

const inputFolder = "./sc-input";
const codeFolder = "./sc-code";

// get Web3
if (typeof web3 !== 'undefined') {
    web3 = new Web3(web3.currentProvider);
} else {
    // set the provider you want from Web3.providers
    web3 = new Web3(new Web3.providers.HttpProvider(RPC_URI));
}

// check web3 connection
//if(!web3.isConnected())
    //throw new Error('unable to connect to ethereum node at ' + RPC_URI);
console.log('connected to ehterum node at ' + RPC_URI);

// set eth
const eth = web3.eth;

/*
var coinbase = web3.eth.coinbase;
console.log('coinbase:' + coinbase);
var balance = web3.eth.getBalance(coinbase);
console.log('balance:' + web3.fromWei(balance, 'ether') + " ETH");
var accounts = web3.eth.accounts;
console.log(accounts);
*/

function hexstrToBytes(str) {
    if (!str)
        return new Uint8Array();

    //omit prifix
    if(str.length > 2 && str.substr(0, 2) == "0x")
        str = str.substr(2);

    var a = [];
    for (var i = 0, len = str.length; i < len; i+=2) {
        a.push(parseInt(str.substr(i,2),16));
    }

    return new Uint8Array(a);
}

function mkContractAddr(sender, nonce){
    return "0x" + web3.utils.sha3(RLP.encode([sender,nonce])).slice(12).substring(14)
}

function parseContract(tx){
    "use strict";
    try{
        //check if tx create contract
        if(!(tx.to == null && tx.input))
            return;

        //basic info
        let addr = mkContractAddr(tx.from, tx.nonce);
        console.log("Get contract " + addr + " from Block#" + tx.blockNumber + "[" + tx.transactionIndex + "] " + 
                "\n\t" + "hash: " + tx.hash + 
                "\n\t" + "from: " + tx.from +
                "\n\t" + "nonce: " + tx.nonce +
                "\n\t" + tx.input.substring(0, 18));  //always 0x60606040???

        //save sc input
        let filename = inputFolder + "/" + addr;
        //let data = new Buffer(hexstrToBytes(tx.input));
        let data = tx.input.substring(2);
        fs.writeFile(filename, data, function (err) {
            if (err) return console.log("save sc input error: " + err);
        });

        //save sc code
        console.log("get code of " + addr);
        sleep.msleep(1);
        eth.getCode(addr, eth.defaultBlock, (err, code) => {
            if(err){
                console.log("get code of " + addr + " error: " + err);
                return;
            }

            if(!code || code == "0x"){
                console.log("get code of " + addr + ": empty contract, not save");
                return;
            }

            //save file
            let filename = codeFolder + "/" + addr;
            let data = code.substring(2);
            fs.writeFile(filename, data, function (err) {
                if (err) return console.log("save sc code error: " + err);
            });
        });
    }
    catch(ex){
        console.log("Save contract error: " + ex);
    }
}

function _getTransactionFromBlock(block, idx, count){
    if(idx >= count)
        return;

    sleep.msleep(1)

    eth.getTransactionFromBlock(block, idx, function(err, tx){
        if(err){
            console.log("get tranction from Block#" + block + "[" + idx + "] error: " + err);
            sleep.sleep(1);
        }
        else{
            //console.log("Block#" + i + "[" + j + "] " + tx.hash);
            parseContract(tx);
        }

        //next
        _getTransactionFromBlock(block, idx + 1, count);
    });
}

function loopTransactionFromBlock(block, count){
    _getTransactionFromBlock(block, 0, count);
}

function _getBlock(idx, end){
    if(idx >= end)
        return;

    sleep.msleep(1)

    eth.getBlockTransactionCount(idx, function(err, tx_count){
        if(err){
            console.log("get tranction count of block#" + idx + " error: " + err);
            sleep.sleep(1);
        }
        else{
            //console.log("Block#" + i + " has " + tx_count + " transactions.");
            loopTransactionFromBlock(idx, tx_count);
        }

        //next block
        _getBlock(idx + 1, end);
    });
}

function loopBlock(begin, end){
    _getBlock(begin, end);
}


//var begin = 1428757;
//var end = begin + 1000;
var begin = parseInt(process.argv[2], 10);
var end = parseInt(process.argv[3], 10);
console.log("get contract from block in range [" + begin + ", " + end + ")");
loopBlock(begin, end);
    
