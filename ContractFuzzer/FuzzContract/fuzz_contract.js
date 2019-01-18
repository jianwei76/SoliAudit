const fs = require('fs');

var accountlist;
var name;
var testSC;
var abi;
var function_name;
var inputParameters;
var returnOutput;
var contractName;
var methodsName;
var inputValues;
var isNumericInput;
var etherFunction = [];
var callEtherFunction = '';
var callEtherFunctionInput;

function fuzz_contract(account, cname, testSrc, tester_abi) {
    accountlist = account;
    abi = tester_abi;
    testSC = testSrc;
    name = cname;


    function_name = null;
    inputParameters = null;
    returnOutput = null;
    contractName = null;
    methodsName = null;
    inputValues = null;
    isNumericInput = null;
    etherFunction = [];
    callEtherFunction = '';
    callEtherFunctionInput = null;

    findEtherFunciton();
}


//find function which use transfer or send or call.value
function findEtherFunciton() {

    var lines = testSC.split('\n');
    let functin_name_line = '';
    //find function blocks
    for (let g in lines) {

        //find keywork 'function'
        if (lines[g].indexOf('function') >= 0)
            functin_name_line = lines[g].split('(')[0].split('function')[1].trim();

        //chekc this three cmd and push the function into array
        if ((lines[g].indexOf('.transfer(') >= 0 || lines[g].indexOf('.send(') >= 0 || lines[g].indexOf('.value(') >= 0) && etherFunction.indexOf(functin_name_line) == -1)
            etherFunction.push(functin_name_line);


    }
}

fuzz_contract.prototype.getFuzzContractName = function getFuzzContractName() {
    return `:fuzz_${name}_main`;
}


fuzz_contract.prototype.genereateFuzzContract = function genereateFuzzContract() {



    var fuzzContract = 'pragma solidity ^0.4.21;\n';


    //generateTestContractInterface
    fuzzContract = fuzzContract + generateTestContractInterface();

    fuzzContract = fuzzContract + `contract fuzz_${name}_main{
    ${name}_interface public ${name};
    function fuzz_${name}_main (address _address) payable{
        ${name} = ${name}_interface(_address);
      }\n`;

    //console.log(abi);
    contractName = name;
    for (var i = 0; i < abi.length; i++) {

        //generate method if input has int generate
        //if (abi[i].type == "function" && abi[i].stateMutability != 'view' && abi[i].stateMutability != 'pure') {
        if (abi[i].type == "function" && abi[i].stateMutability != 'pure') {

            isNumericInput = false;
            function_name = abi[i].name;
            let ori_function_name = abi[i].name;
            inputParameters = setInputParameterFormat(abi[i].inputs);
            //console.log('abi[i].name:', abi[i].name, "  input:", abi[i].inputs);
            if (abi[i].outputs.length != 0) {
                returnOutput = 'returns (' + setOutputParameterFormat(abi[i].outputs) + ')';
            } else
                returnOutput = '';



            methodsName = abi[i].name;
            inputValues = setValuesFormat(abi[i].inputs);


            fuzzContract = fuzzContract + setFunctionCall(abi[i].payable);

            //console.log(setFunctionCall(abi[i].payable));

            if (isNumericInput) {
                function_name = ori_function_name + '_overflow';
                inputParameters = setInputParameterFormat(abi[i].inputs);
                inputValues = setOverFlowValues(abi[i].inputs);
                fuzzContract = fuzzContract + setFunctionCall(abi[i].payable);
                function_name = ori_function_name + '_underflow';
                inputParameters = setInputParameterFormat(abi[i].inputs);
                inputValues = setUnderFlowValues(abi[i].inputs);
                fuzzContract = fuzzContract + setFunctionCall(abi[i].payable);
            }

            //console.log(etherFunction,'------',abi[i].name , '----',etherFunction.indexOf(abi[i].name));
            if (etherFunction.indexOf(abi[i].name) > -1) {
                callEtherFunctionInput = setFallBackInput(abi[i].inputs);
                callEtherFunction += `if(${contractName}.balance >= msg.value && msg.value>0 && gasleft() >=100000)  { callfallback(${contractName}.balance,msg.value,count); ${contractName}.${methodsName}(${callEtherFunctionInput});}\n`

            }
        }
    }


    var fallback = `
    event callfallback(uint balance ,uint value,uint count);
    uint count=0;
    function () payable {
    count++;
    ${callEtherFunction}
  }
}`;


    fuzzContract = fuzzContract + fallback;
    return fuzzContract;
}


function setFallBackInput(parameters) {

    let returnFormat = [];

    for (let j = 0; j < parameters.length; j++) {
        let type = parameters[j].type;
        if (type == 'address') {
            // returnFormat.push(accountlist[0]);
            returnFormat.push("address(this)");
        } else if (parameters[j].type.startsWith('uint') == true) {
            returnFormat.push('1000000000000000000');
        } else if (type.startsWith('address[]') == true) {
            returnFormat.push(accountlist.slice(0, 1));
        } else if (type == 'string') {
            returnFormat.push('test');
        } else if (type == 'bool') {
            returnFormat.push('True');
        }

    }
    return returnFormat.join(',');
}


//generate test contract interface

function setFunctionCall(payable) {

    var returnFunction = '';

    var payable_template = `
  function ${function_name}(${inputParameters}) payable ${returnOutput} {
          ${contractName}.${methodsName}.value(msg.value)(${inputValues});
  }`;


    var nonpayable_template = `
  function ${function_name}(${inputParameters}) ${returnOutput}{
    ${contractName}.${methodsName}(${inputValues});
  }`;

    if (payable) {
        returnFunction = payable_template;
    } else {
        returnFunction = nonpayable_template;
    }


    return returnFunction;
}


function setInputParameterFormat(parameters) {

    let returnFormat = [];
    for (let j = 0; j < parameters.length; j++) {
        let type = parameters[j].type;
        if (parameters[j].type.startsWith('uint') == true) {
            isNumericInput = true;
            if (function_name.endsWith('_underflow') || function_name.endsWith('_overflow')) {
                type = 'string';
                returnFormat.push(type + ' extreme_flow' + j);
            } else {
                if (parameters[j].name == '')
                    returnFormat.push(type + ' InputVal' + j);
                else
                    returnFormat.push(type + ' ' + parameters[j].name);
            }
        } else {
            if (parameters[j].name == '')
                returnFormat.push(type + ' InputVal' + j);
            else
                returnFormat.push(type + ' ' + parameters[j].name);
        }


    }

    return returnFormat.join(',');
}

function setOutputParameterFormat(parameters) {

    let returnFormat = [];
    for (let j = 0; j < parameters.length; j++) {
        let type = parameters[j].type;
        if (parameters[j].type.startsWith('uint') == true) {

            if (function_name.endsWith('_underflow') || function_name.endsWith('_overflow')) {
                type = 'string';
                returnFormat.push(type + ' extreme_flow' + j);
            } else {
                if (parameters[j].name == '')
                    returnFormat.push(type + ' OutputVal' + j);
                else
                    returnFormat.push(type + ' ' + parameters[j].name);
            }
        } else {
            if (parameters[j].name == '')
                returnFormat.push(type + ' OutputVal' + j);
            else
                returnFormat.push(type + ' ' + parameters[j].name);
        }


    }

    return returnFormat.join(',');
}

function setValuesFormat(parameters) {

    let returnFormat = [];
    for (let j = 0; j < parameters.length; j++) {
        if (parameters[j].name == '')
            returnFormat.push('InputVal' + j);
        else
            returnFormat.push(parameters[j].name);

    }
    return returnFormat.join(',');
}

function setOverFlowValues(parameters) {

    let returnFormat = [];
    for (let j = 0; j < parameters.length; j++) {

        if (parameters[j].type.startsWith('uint') == true)
            returnFormat.push('2**' + parameters[j].type.slice(4) + '-1');
        else
            returnFormat.push(parameters[j].name);

    }
    return returnFormat.join(',');
}

function setUnderFlowValues(parameters) {

    let returnFormat = [];
    for (let j = 0; j < parameters.length; j++) {
        if (parameters[j].type.startsWith('uint') == true)
            returnFormat.push('0');
        else
            returnFormat.push(parameters[j].name);


    }
    return returnFormat.join(',');
}


function generateTestContractInterface() {

    var test_interface = 'contract ' + name + '_interface {\n';
    for (var i = 0; i < abi.length; i++) {

        function_name = abi[i].name;
        //if (abi[i].type == "function" && abi[i].stateMutability != 'view' && abi[i].stateMutability != 'pure') {
        if (abi[i].type == "function" && abi[i].stateMutability != 'pure') {

            if (abi[i].payable == true)
                test_interface += 'function ' + abi[i].name + '(inputParameter) returnValues payable {}\n';
            else
                test_interface += 'function ' + abi[i].name + '(inputParameter) returnValues {}\n';

            test_interface = test_interface.replace('inputParameter', setInputParameterFormat(abi[i].inputs));

            if (abi[i].outputs.length != 0)
                test_interface = test_interface.replace('returnValues', 'returns(' + setOutputParameterFormat(abi[i].outputs) + ')');
            else
                test_interface = test_interface.replace('returnValues', '');
        }

    }

    test_interface = test_interface + '}\n';
    return test_interface;
}

module.exports = fuzz_contract;