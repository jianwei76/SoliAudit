var fs = require('fs');
var removeEmptyLines = require("remove-blank-lines");

var functionblock = [];
var block = '';
var stack = [];
var InFun = false;
var insertedEvent=[];

function setEvent() {
     functionblock = [];
     block = '';
     stack = [];
     InFun = false;
     insertedEvent=[];
}



//readine and find function block with pattern function{xxxxx}
function findblock(line) {

    //check function block exist
    if ((line.indexOf('function') >= 0 || line.indexOf('modifier') >= 0) && line.indexOf('pure') < 0  && !line.trim().startsWith('*')) {
        block = '';
        InFun = true;

    }

    //if function exist the use stack to check {   }
    if (InFun == true) {

        //rebuild the function block
        block = block + line + '\n';

        if (line.indexOf('{') >= 0) {
            stack.push('{');
        }

        if (line.indexOf('}') >= 0) {
            if (stack.length == 0) {

                InFun = false;
                block = '';
                return;
            }

            if (stack.length > 0) {
                stack.pop('{');
                if (stack.length == 0) {
                    InFun = false;
                    functionblock.push(block);
                    block = '';
                }
            }
        }
    }
}


function add(block) {
    //console.log(block,'-------');
    for (var i = 0; i < block.length; i++) {

        if (block.charAt(i) == '(')
            stack.push('(');

        if (block.charAt(i) == ')') {
            stack.pop('(');

            if (stack.length == 0) {
                return block.slice(0, i + 1) + "\n{\n" + block.slice(i + 1) + '\n}\n';
            }
        }

    }
     return block;
}


// add {} to one line if else statement and remove comments
function preprocess(contract) {

    //replace /r/n with /n
    contract = contract.replace(/\r\n/g, '\n');

    //remove comments
    contract = contract.replace(/(\/\*)(.|\n)*?(\*\/)/g, '');
    contract = contract.replace(/(\/\/)(.)*/gi, '');

    //replace multiline if condition 
    var multiline_if = /(?=if[\W])(.|\n)*?(\s|\n)*?({|;)/g;
    var multiline_if_block = contract.match(multiline_if);
    for (let b in multiline_if_block) {
        var temp_multiline_if_block = multiline_if_block[b].replace(/\n/g, '');
        contract = contract.replace(multiline_if_block[b], temp_multiline_if_block);
    }

    //replace multiline require condition 
    var multiline_require = /(?=require)(.|\n)*?\);/g;
    var multiline_require_block = contract.match(multiline_require);
    for (let b in multiline_require_block) {
        var temp_multiline_require_block = multiline_require_block[b].replace(/\n/g, '');
        contract = contract.replace(multiline_require_block[b], temp_multiline_require_block);
    }


    //replace one line { }
    contract = contract.replace(/{/g, '\n{\n');
    contract = contract.replace(/}/g, '\n}\n');

    var semicolon = /^(?!\s*for).*;/mg;
    var semicolon_line = contract.match(semicolon);


    //replace one line :
    for (let s in semicolon_line) {
        var temp_semi = semicolon_line[s].replace(/\;/mg, '\;\n');
        contract = contract.replace(semicolon_line[s], temp_semi);
    }

    //find one line if else while for statement
    var oneline_if_regex = /\s*(if|else|while|for)[^{]*?.*;\s*\n/mg;
    var block = contract.match(oneline_if_regex);

    //add {} to one line if else while statement
    for (let b in block) {

        var line = block[b].match(/.*\;/g);
        var temp_line = '';

        var last_line = line[line.length - 1];
        if (last_line.includes('if') == true || last_line.includes('for') == true || last_line.includes('while') == true) {
            temp_line = add(last_line);
            contract = contract.replace(last_line, temp_line);
        } else if (last_line.includes('else')) {
            temp_line = last_line.replace(/else/, 'else \n{\n');
            temp_line = temp_line + '\n}\n';
            contract = contract.replace(last_line, temp_line);
        } else {
            temp_block = block[b].replace(last_line, '\n{\n' + last_line + '\n}\n')
            contract = contract.replace(block[b], temp_block);
        }
    }
    return contract;
}

setEvent.prototype.insert = function insert(fileContent) {


    //read contract and preprocess
    var contract = preprocess(fileContent);
    var lines = contract.split('\n');

    //find function blocks
    for (let g in lines) {
        findblock(lines[g]);
    }

    var function_array = functionblock;
    var eventNum = 0;
    var eventCllect = [];
    var temp_eventCllect = [];
    var function_anchor = '';

    for (let i in function_array) {
        var line_regex = /.*\n/ig;
        var line = function_array[i].match(line_regex);
        function_anchor = function_array[i];
        temp_eventCllect = [];
        temp_functionblock = '';

        for (var j in line) {

            var return_type;

            //for strange return format
            if (line[j].includes('returns')) {
                let regx = /\((.*?)\)/sig;
                let return_value = line[j].match(regx);
                if (return_value.length == 1) {
                    return_type = return_value[0].split(' ')[0].replace('(', '').replace(')', '');
                } else {
                    return_type = return_value[return_value.length-1].split(' ')[0].replace('(', '').replace(')', '');
                }
            }


            if (line[j].includes(';') == true) {

                if (line[j].includes('while') == true || line[j].replace(/\s/g, '').includes('for(') == true || line[j].trim().startsWith('//') == true || line[j].trim().replace(/\s/g, '').startsWith(');') == true) {

                    temp_functionblock = temp_functionblock + line[j];
                    continue;
                }

                if (line[j].match(/return.*\S;/gm) != null) {
                    //insert event to get return value;
                    eventNum++;
                    let eventFun = 'event_return' + eventNum + "(" + return_type + " val);\n";
                    let Insert_eventFun = 'event_return' + eventNum + "(" + line[j].replace('return', '').replace(';', '').replace('\n', '').trim() + ");\n";
                    eventCllect.push('event ' + eventFun);
                    temp_eventCllect.push('event ' + eventFun);
                    temp_functionblock = temp_functionblock + Insert_eventFun + line[j];

                } else if(line[j].includes('return') == true || line[j].includes('_;') == true || line[j].includes('break') == true || line[j].includes('continue') == true) {
                    eventNum++;
                    let eventFun = 'event' + eventNum + "();\n";
                    eventCllect.push('event ' + eventFun);
                    temp_eventCllect.push('event ' + eventFun);
                    temp_functionblock = temp_functionblock + eventFun + line[j];

                } else if (line[j].includes('throw') == true || line[j].includes('revert') == true) {
                    // because event log will not show , so unnessary insert event.
                    temp_functionblock = temp_functionblock + line[j];
                } else {
                    eventNum++;
                    let eventFun_start = 'event' + eventNum + "();\n";
                    eventNum++;
                    let eventFun_end = 'event' + eventNum + "();\n";
                    eventCllect.push('event ' + eventFun_start);
                    temp_eventCllect.push('event ' + eventFun_start);
                    eventCllect.push('event ' + eventFun_end);
                    temp_eventCllect.push('event ' + eventFun_end);
                    temp_functionblock = temp_functionblock + eventFun_start + line[j] + eventFun_end;

                }
            } else {
                temp_functionblock = temp_functionblock + line[j];
            }
        }
        contract = contract.replace(function_anchor, temp_eventCllect.join("") + temp_functionblock);
    }

    insertedEvent = eventCllect;
    return removeEmptyLines(contract.toString());
}




setEvent.prototype.getInsertedEvent = function getInsertedEvent() {

    return insertedEvent;
}


module.exports = setEvent;

