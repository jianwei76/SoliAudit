const express = require('express');
const bodyParser = require('body-parser');
const app = express();
var multer = require('multer');
var upload = multer();
const FuzzMain = require('./FuzzMain.js');
var mp = require('./MessageProducer.js');


app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());
app.use('/report', express.static(__dirname + '/report'));

app.post('/csf/task/upload', upload.array('sampleFile'), (req, res) => {


    let ip = req.connection.remoteAddress;
    mp.init(ip);

    let taskid = req.body.taskId;
    let initialEther = req.body.a_InitialEther;
    let fuzz_amount = req.body.a_FuzzAmount;
    let tester_contractSRC = req.files[0].buffer.toString();
    let tester_contractName = req.body.a_ContractName;
    let sequence = req.body.a_Sequence.split(",").map(String);
    let returnJson = {
        "taskId": taskid,
        "status": "SUCCESS",
        "message": ''
    };
    
    console.log('form initialEther', initialEther);
    console.log('form fuzz_amount', fuzz_amount);
    ///console.log('form tester_contractSRC', tester_contractSRC);
    console.log('form tester_contractName', tester_contractName);
    console.log('form sequence', sequence);
    console.log('returnJson=', returnJson);
    res.status(200).send(returnJson);
    let fm = new FuzzMain(mp, taskid, initialEther, fuzz_amount, tester_contractSRC, tester_contractName, sequence);
    fm.startFuzz();
    console.log('Finish');

});

app.listen(2020, () => console.log('Example app listening on port 2020!'))