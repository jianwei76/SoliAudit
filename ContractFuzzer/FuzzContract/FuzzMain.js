const Web3 = require('web3');
const fs = require('fs');
const solc = require('solc');
const HashMap = require('hashmap');
const setEvent = require('./event.js');
const fuzzinput = require('./fuzz-input.js');
const nodeUnique = require('node-unique-array')
const fuzz_contract = require('./fuzz_contract.js');
const log4js = require("log4js");
const log4js_config = require("./log4j.json");
log4js.configure(log4js_config);
const verify_result = require('./verify_result.js');
const countArr = require('count-array-values')
const mkdirp = require('mkdirp');
var ip = require("ip");
var zipFolder = require('zip-folder');
const _ = require('underscore');
var mp = null;
// connect to ethereum node 
const ethereumUri = 'http://ganache:8545';
var web3 = new Web3();
web3.setProvider(new web3.providers.HttpProvider(ethereumUri));

//initial variable
var AllTargets = [];
var fallBcakEvent = [];
var results = {};
var error_results = {};
var Summary = {};
var interval_switch = false;
var tempResult_map = new HashMap();
var tempEvent_map = new HashMap();
var uniqueNormalEvent = new nodeUnique();
var uniqueFunctionName = new nodeUnique();
var error_key_round = [];
var tester_myContractEvent = null;
var fuzzer_myContractEvent = null;
var eventCollects = [];
var startblock = 0;
var initialEther = 0;
var fuzz_amount = 0;
var order = [];
var taskid = '';
var ip_address = process.env.host;
var port = process.env.port;
console.log('ip_address:',ip_address);
console.log('ip_address:',port);

function setFuzzer(mpv, tid, InitialEeather, FuzzAmount, ContractSRC, ContractName, Sequence) {

    initialEther = InitialEeather;
    fuzz_amount = FuzzAmount;
    tester_contractSRC = ContractSRC;
    tester_contractName = ContractName;
    order = Sequence;
    taskid = tid;
    AllTargets = [];
    fallBcakEvent = [];
    results = {};
    error_results = {};
    Summary = {};
    interval_switch = false;
    tempResult_map = new HashMap();
    tempEvent_map = new HashMap();
    uniqueNormalEvent = new nodeUnique();
    uniqueFunctionName = new nodeUnique();
    error_key_round = [];
    tester_myContractEvent = null;
    fuzzer_myContractEvent = null;
    eventCollects = [];
    startblock = 0;
    mp = mpv;
}

setFuzzer.prototype.startFuzz = function startFuzz() {

//console.time('test');

    try {
        if (!web3.isConnected()) {
            throw new Error('unable to connect to ethereum node at ' + ethereumUri);
        } else {
            console.log('connected to ehterum node at ' + ethereumUri);
            let coinbase = web3.eth.coinbase;
            console.log('coinbase:' + coinbase);
            let balance = web3.eth.getBalance(coinbase);
            console.log('balance:' + web3.fromWei(balance, 'ether') + " ETH");
            var accounts = web3.eth.accounts;
            console.log(accounts);

            var account_one = accounts[0];
            var account_two = accounts[1];
            var account_three = accounts[2];

        }

        //get current block number for retriveing event
        startblock = web3.eth.blockNumber;

        //insert events to tester contract
        let insertE = new setEvent();
        let insertedContract = insertE.insert(tester_contractSRC);
        eventCollects = insertE.getInsertedEvent();
        let source = insertedContract;

        //compile tester contract and write error message
        console.log(source);
        console.log('Compiling contract...');
        let compiledContract = solc.compile(source);
        console.log('Compiling done');
        console.log(compiledContract);
        console.log('Compiled error result:', compiledContract.errors);
        //writeResults(compiledContract.errors, './results/' + tester_contractName + '/', 'tester_compileError.txt');

        // code and ABI that are needed by web3 
        let tester_bytecode = compiledContract.contracts[':' + tester_contractName].bytecode;
        let tester_abi = JSON.parse(compiledContract.contracts[':' + tester_contractName].interface);

        //if compile success we can deploy
        if (tester_bytecode) {

            let tester_gasEstimate = web3.eth.estimateGas({ data: '0x' + tester_bytecode, value: web3.toWei(initialEther, 'ether') });
            let tester_MyContract = web3.eth.contract(tester_abi);
            console.log('Deploying contract.....name:' + tester_contractName, ' use gas:', tester_gasEstimate);

            //start deploy tester contract
            let tester_myContractReturned = tester_MyContract.new({
                from: account_one,
                data: '0x' + tester_bytecode,
                gas: tester_gasEstimate + 100000,
                value: web3.toWei(initialEther, 'ether')
            }, function(err, tester_myContract) {

                if (!err) {

                    // NOTE: The callback will fire twice!
                    // Once the contract has the transactionHash property set and once its deployed on an address.
                    // e.g.  check tx hash on the first call (transaction send)

                    if (!tester_myContract.address) {
                        console.log(tester_contractName + `.transactionHash = ${tester_myContract.transactionHash}`);
                    } else {

                        //tester contract deploy success
                        tester_myContractEvent = tester_myContract;
                        console.log(tester_contractName + `.address = ${tester_myContract.address}`); // the contract address
                        console.log('Deploy ' + tester_contractName + ' finish \n');

                        //Generate fuzzer contract
                        var fuzzContractGen = new fuzz_contract(accounts.slice(1, 3), tester_contractName, tester_contractSRC, tester_abi);
                        var fuzzer_contractName = fuzzContractGen.getFuzzContractName();
                        var fuzzer_contract = fuzzContractGen.genereateFuzzContract();

                        //compile fuzzer contract and write error message
                        console.log('Compiling fuzzer contract contract...');
                        let compiledContract = solc.compile(fuzzer_contract);
                        console.log(fuzzer_contract);
                        console.log('Compiling fuzzer contract done');
                        //console.log('Compiled error result:', compiledContract.errors);
                        //writeResults(compiledContract.errors, './results/' + tester_contractName + '/', 'fuzzer_compileError.txt');


                        let fuzzer_bytecode = compiledContract.contracts[fuzzer_contractName].bytecode;
                        let fuzzer_abi = JSON.parse(compiledContract.contracts[fuzzer_contractName].interface);

                        //if compile success we can deploy
                        if (fuzzer_bytecode) {

                            //start deploy fuzzer contract
                            let fuzzer_gasEstimate = web3.eth.estimateGas({ data: '0x' + fuzzer_bytecode });
                            let fuzzer_MyContract = web3.eth.contract(fuzzer_abi);
                            console.log('Deploying contract.....name:' + fuzzer_contractName, ' use gas:', fuzzer_gasEstimate);

                            let fuzzer_myContractReturned = fuzzer_MyContract.new(tester_myContract.address, {
                                from: account_one,
                                data: '0x' + fuzzer_bytecode,
                                value: 100000000000000000000000,
                                gas: fuzzer_gasEstimate + 100000,
                            }, function(err, fuzzer_myContract) {

                                if (!err) {

                                    // NOTE: The callback will fire twice!
                                    // Once the contract has the transactionHash property set and once its deployed on an address.
                                    // e.g.  check tx hash on the first call (transaction send)

                                    if (!fuzzer_myContract.address) {
                                        console.log(fuzzer_contractName + `.transactionHash = ${fuzzer_myContract.transactionHash}`);
                                    } else {


                                        //fuzzer contract deploy success
                                        fuzzer_myContractEvent = fuzzer_myContract;
                                        console.log(fuzzer_contractName + `.address = ${fuzzer_myContract.address}`); // the contract address
                                        console.log('Deploy ' + fuzzer_contractName + ' finish \n');


                                        //set fuzzer schedluer and fuzz generator
                                        getMethods(fuzzer_myContract, tester_myContract);
                                        let scheduler = orderScheduler();
                                        var fzinput = new fuzzinput(accounts);
                                        var fuzz_count = 0;

                                        //console.log('Total fuzz amount:', getSchedulerAmount(scheduler));

                                        //start fuzz
                                        console.log('Start fuzz');
                                        console.log(scheduler);
                                        for (let i = 0; i < fuzz_amount; i++) {


                                            let round = 'round' + (i + 1);
                                            results[round] = {};
                                            var round_result = {};

                                            for (let s in order) {

                                                //if function name with _overflow or _underflow do not fuzz not, it will fuzz within original function
                                                // if (scheduler[s].name.includes('_overflow') || scheduler[s].name.includes('_underflow'))
                                                //     continue;

                                                //initialize result json 
                                                results[round] = round_result;
        
                                                let key = order[s];

                                                // a function give args then return fuzz input array
                                                let fuzzOBJ = getSendOBJ(scheduler, order[s], round);
                                                let sendTx = fuzzOBJ.functionOBJ.sendTransaction;
                                                let input = fzinput.generate(fuzzOBJ);
                                                var txHash = '';
                                                try {
                                                    //console.log('balance:', web3.eth.getBalance(tester_myContract.address));
                                                    //console.log('fuzzbalance:', web3.eth.getBalance(fuzzer_myContract.address));
                                                    txHash = sendTx.apply(null, input);
                                                } catch (err) {
                                                    console.log(err);
                                                    console.log('err txHash', txHash);
                                                }

                                                if (txHash != '') {

                                                    //for record tx receipt.status 
                                                    let tempReslt = {};
                                                    //for record event of function return value
                                                    let tempReslt2 = {};

                                                    //record the function info for getting result later
                                                    fuzz_count++;
                                                    tempReslt.txHash = txHash;
                                                    tempReslt.funName = fuzzOBJ.name.replace(/_.*flow/gm, '');
                                                    tempReslt.input = input
                                                    tempReslt.key = key;
                                                    tempReslt.round = round;
                                                    tempResult_map.set(txHash, tempReslt);

                                                    //record the function info which have return value for getting event later
                                                    if (fuzzOBJ.outputs.length > 0) {
                                                        tempReslt2.txHash = txHash;
                                                        tempReslt2.funName = fuzzOBJ.name.replace(/_.*flow/gm, '');
                                                        uniqueFunctionName.add(fuzzOBJ.name.replace(/_.*flow/gm, ''))
                                                        tempReslt2.input = input
                                                        tempReslt2.round = round;
                                                        tempEvent_map.set(txHash, tempReslt2);
                                                    }
                                                    console.log('NO.', fuzz_count, ',fuzz ', tempReslt.funName, ' transcations');
                                                }
                                            }
                                        }
                                        console.log('==============Start get result ==============');
                                        interval_switch = setInterval(getResult, 5000);
                                    }

                                    // Note that the returned "myContractReturned" === "myContract",
                                    // so the returned "myContractReturned" object will also get the address set.

                                } else {
                                    console.log('Error ContractName:' + fuzzer_contractName);
                                    console.log(err);
                                }
                            });
                        }
                    }

                    // Note that the returned "myContractReturned" === "myContract",
                    // so the returned "myContractReturned" object will also get the address set.
                } else {
                    console.log('Error ContractName:' + tester_contractName);
                    console.log(err);
                }

            });

        }

        return true;
    } catch (error) {
        console.log('error:', error.stack.split("\n", 1).join(""));
        snedReturnJson('FAIL', error.stack.split("\n", 1).join(""), '');

    }
}


function orderScheduler() {

    var target = [];
    if (order.length == 0) {

        target = AllTargets.sort(function(a, b) {
            //console.log(a[0].name ,'---',a[0].stateMutability);
            if (a.stateMutability < b.stateMutability) {
                return -1;
            }
            if (a.stateMutability > b.stateMutability) {
                return 1;
            }
            return 0;
        });
    } else {
        for (var i = 0; i < order.length; i++) {
            //element => element.name == funcname + '_underflow' || element.name == funcname + '_overflow' || element.name == funcname
            let temp_target = AllTargets.filter(element => element.name == order[i] + '_underflow' || element.name == order[i] + '_overflow' || element.name == order[i]);

            for (var j = 0; j < temp_target.length; j++) {
                target.push(temp_target[j])
            }
        }
    }

    target = _.uniq(target);
    return target;
}


//get function object
function getSendOBJ(scheduler, funcname, round) {

    let returnOBJ;
    obj = scheduler.filter(element => element.name == funcname + '_underflow' || element.name == funcname + '_overflow' || element.name == funcname);
    obj = obj.sort((a, b) => b.name.length - a.name.length);
    if (obj.length >= 3) {
        if (round == 'round1') {
            returnOBJ = obj[0];
        } else if (round == 'round2') {
            returnOBJ = obj[1];
        } else {
            let r = Math.floor(Math.random() * obj.length);
            returnOBJ = obj[r];
        }
    } else if (obj.length == 2) {
        let r = Math.floor(Math.random() * obj.length);
        returnOBJ = obj[r];
    } else {
        returnOBJ = obj[0];
    }
    return returnOBJ;


}


//get scheduler total amount
function getSchedulerAmount(scheduler) {

    let total = 0;
    total += (scheduler.length * fuzz_amount)
    return total;
}


//watch return event to find abnormal and  calculate converage 
function watchEvent() {
    let fuzzer = fuzzer_myContractEvent.callfallback({}, { fromBlock: startblock, toBlock: 'latest' });
    let tester = tester_myContractEvent.allEvents({ fromBlock: startblock, toBlock: 'latest' });


    //get fuzzer event 
    let fuzzerResults = fuzzer.get(function(error, results) {

        let isReentrancy = false;
        let ReentrancyTx = '';
        if (!error) {
            results.forEach(function(result) {
                if (result.event.startsWith('callfallback')) {
                    fallBcakEvent.push(result.transactionHash);
                }
            });

            countArr(fallBcakEvent).map(function(x) {
                if (x.count >= 2) isReentrancy = true;
                ReentrancyTx = x.value
            });

            if (isReentrancy) {
                Summary.ReentrancyProblem = ReentrancyTx;
            }
        } else {
            console.log(error);
        }

        console.log('Finish get event');
    });

    //get tester event 
    let testerResults = tester.get(function(error, results) {

        if (!error) {

            results.forEach(function(result) {

                if ('event' in result) {
                    if (result.event.startsWith('event')) {
                        uniqueNormalEvent.add(result.event);

                        if (result.event.startsWith('event_return')) {
                            let temp_val = tempEvent_map.get(result.transactionHash);
                            temp_val.returnVal = result.args.val.toString(10);
                            tempEvent_map.set(result.transactionHash, temp_val);
                        }
                    }
                }

            });

            //calculate coverage
            Summary.coverage = 100 * (uniqueNormalEvent.size() / eventCollects.length).toPrecision(4) + '%';

            //find abnormal result
            var find_abnorml = new verify_result();
            let returnValueDataset = tempEvent_map.values().filter(function(item) {
                return !(item.returnVal == null);
            });

            Summary.AbnormalResult = find_abnorml.findUnNormal(returnValueDataset, uniqueFunctionName);

            console.log('Finish tester event');
            writeResults();
        } else {
            console.log(error);
        }
    });

    testerResults.stopWatching();
    fuzzerResults.stopWatching();
}

function snedReturnJson(status, message, link) {

    let returnJson = {
        taskId: taskid,
        status: status,
        message: message,
        link: link
    };

    console.log(JSON.stringify(returnJson));
    mp.sendMessage(JSON.stringify(returnJson));
}



//a function run by setinterval to get result from receipt and write to file 
function getResult() {

    console.log(tempResult_map.size + ' transcations left');

    tempResult_map.forEach(function(value, key) {
        let receipt = web3.eth.getTransactionReceipt(key);

        if (receipt) {
            tempResult_map.delete(key);
            value.status = receipt.status
            let index = value.key;
            let round = value.round;
            delete value.key;
            delete value.round;
            results[round][index] = value;

            if (receipt.status == '0x0') {
                error_key_round.push({ index, round });
            }
        }

    });

    if (tempResult_map.size == 0) {

        clearInterval(interval_switch);
        console.log('==============End get result ==============');

        for (let i = 0; i < error_key_round.length; i++) {

            let error_key = error_key_round[i].index;
            let error_round = error_key_round[i].round;

            if (!(error_round in error_results)) {
                error_results[error_round] = {};
            }

            error_results[error_round][error_key] = results[error_round][error_key];
        }

        watchEvent();

    }
}


//write to file 
function writeResults() {

    console.log('start write reuslt');
    let path2 = './results/' + tester_contractName + '/';

    mkdirp(path2, function(err) {
        if (err) console.error(err);
        else {
            fs.writeFile(path2 + 'Summary.json', JSON.stringify(Summary, null, 4), function(err) {

                if (err) {
                    console.log(err);
                } else {

                    mkdirp(path2, function(err) {
                        if (err) console.error(err);
                        else {
                            fs.writeFile(path2 + 'ErrorResults.json', JSON.stringify(error_results, null, 4), function(err) {
                                if (err) {
                                    console.log(err);
                                } else {

                                    mkdirp(path2, function(err) {
                                        if (err) console.error(err);
                                        else {
                                            fs.writeFile(path2 + 'AllResults.json', JSON.stringify(results, null, 4), function(err) {
                                                if (err) {
                                                    console.log(err);
                                                } else {

                                                    zipFolder('./results/' + tester_contractName, './report/' + taskid + '.zip', function(err) {
                                                        if (err) {
                                                            console.log('Error on zip reuslt floder', err);
                                                        } else {
                                                            console.log('Finsh zip reuslt floder');
                                                            snedReturnJson('SUCCESS', '', 'http://' + ip_address +':'+port+'/report/' + taskid + '.zip');
                                                            console.log("JSON saved");
                                                            console.log('All Finish');
                                                                                                                   }
                                                    });

                                                    //console.timeEnd('test');
                                                }
                                            });
                                        }
                                    });
                                }
                            });
                        }
                    });
                }
            });
        }
    });



}


// get methods from  deployed contract
function getMethods(fuzzer_obj, tester_obj) {

    fuzzer_obj.abi.forEach(function(interface) {
        //if (interface.type == "function"  && interface.stateMutability != 'pure') {

        if (interface.type == "function" && interface.stateMutability != 'view' && interface.stateMutability != 'pure') {
            let Targets = {};
            Targets.name = interface.name;
            Targets.args = interface.inputs;
            Targets.functionOBJ = fuzzer_obj[interface.name];
            Targets.outputs = interface.outputs;
            Targets.stateMutability = interface.stateMutability;
            AllTargets.push(Targets);
        }
    });

    tester_obj.abi.forEach(function(interface) {
        //if (interface.type == "function"  && interface.stateMutability != 'pure') {

        if (interface.type == "function" && interface.stateMutability != 'view' && interface.stateMutability != 'pure') {
            let Targets = {};
            Targets.name = interface.name;
            Targets.args = interface.inputs;
            Targets.functionOBJ = tester_obj[interface.name];
            Targets.outputs = interface.outputs;
            Targets.stateMutability = interface.stateMutability;
            AllTargets.push(Targets);
        }
    });

}


module.exports = setFuzzer;