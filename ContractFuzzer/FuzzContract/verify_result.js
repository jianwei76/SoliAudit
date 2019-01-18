var minkowski = require('compute-minkowski-distance');
var jsonQuery = require('json-query');
var stats = require("stats-analysis");
const isNumber = require('is-number');

var abnormal_result = [];
function verify_result() {
    abnormal_result=[];
}


verify_result.prototype.findUnNormal = function findUnNormal(data, unique_function) {


    for (var i = 0; i < unique_function.size(); i++) {
   
        let result = jsonQuery(':[*funName=' + unique_function.get(i)[i] + '].returnVal', { data: data }).value;
        let input = jsonQuery(':[*funName=' + unique_function.get(i)[i] + ']', { data: data }).value;
        let abnormal_index;
        let resultArray = [];

        //numeric result
        if (isNumber(result[0])) {
            resultArray = result.map(Number);
            let inputArray = [];
            for (var j = 0; j < input.length; j++) {
                inputArray.push(input[j].input.slice(0, input[j].input.length - 1).map(function(num) {
                    if (num == 'Max value')
                        return 2 ** 256 - 1;
                    else {
                        if (isNumber(num))
                            return parseFloat(num);
                        else
                            return num;
                    }
                }));
            }

            resultArray = resultArray.map(x => new Array(inputArray[0].length).fill(x).fill(0, 1));
            let dist = distance(inputArray, resultArray);
            abnormal_index = stats.indexOfOutliers(dist, stats.outlierMethod.MAD);


        } else {
            resultArray = result.map(String);
            abnormal_index = compressArray(resultArray);
        }

        for (var j = 0; j < abnormal_index.length; j++) {
          abnormal_result.push(input[abnormal_index[j]])
        }

    }
    return abnormal_result;
}


function compressArray(original) {

    var compressed = [];
    // make a copy of the input array
    var copy = original.slice(0);

    let return_index = [];
    let min_count = Number.MAX_SAFE_INTEGER;
    // first loop goes over every element
    for (var i = 0; i < original.length; i++) {
        let min_index = [];
        var myCount = 0;
        // loop over every element in the copy and see if it's the same
        for (var w = 0; w < copy.length; w++) {
            if (original[i] == copy[w]) {
                // increase amount of times duplicate is found
                myCount++;
                // sets item to undefined
                delete copy[w];
                min_index.push(w);
            }
        }

        if (myCount > 0) {
            var a = new Object();
            a.value = original[i];
            a.count = myCount;
            compressed.push(a);

            if (min_count > myCount) {
                return_index = min_index;
                min_count = myCount;
            }
            //  console.log(return_index , ' count :',min_count);
        }
    }

    if (compressed.length == 1)
        return [];
    else
        return return_index;
};



function distance(input, result) {
    let dist = []
    for (var i = 0; i < input.length; i++) {
        dist.push(minkowski(input[i], result[i]));
    }
    return dist;
}


function filterOutliers(someArray) {

    if (someArray.length < 4)
        return someArray;

    let values, q1, q3, iqr, maxValue, minValue;

    values = someArray.slice().sort((a, b) => a - b); //copy array fast and sort
    console.log(values);
    if ((values.length / 4) % 1 === 0) { //find quartiles
        q1 = 1 / 2 * (parseFloat(values[(values.length / 4)]) + parseFloat(values[(values.length / 4) + 1]));
        q3 = 1 / 2 * (parseFloat(values[(values.length * (3 / 4))]) + parseFloat(values[(values.length * (3 / 4)) + 1]));
    } else {
        q1 = parseFloat(values[Math.floor(values.length / 4 + 1)]);
        q3 = parseFloat(values[Math.ceil(values.length * (3 / 4) + 1)]);
    }

    iqr = q3 - q1;
    maxValue = q3 + (iqr * 1.5);
    minValue = q1 - (iqr * 1.5);
    console.log('q3', q3);
    console.log('q1', q1);
    console.log('iqr', iqr);
    console.log('maxValue=', maxValue);
    console.log('minValue=', minValue);
    return values.filter((x) => (parseFloat(x) >= minValue) && (parseFloat(x) <= maxValue));
}




module.exports = verify_result;