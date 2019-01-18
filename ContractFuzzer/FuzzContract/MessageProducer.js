'use strict';
var Stomp = require('stomp-client');
var MessageProducer = function MessageProducer(){
  this._stompClient = null;
};
MessageProducer.prototype.init = function init(mq_server){
	
  this._stompClient = new Stomp(mq_server, 61613);

  this._stompClient.connect(function(sessionId){
    console.log('STOMP client connected.');
  });
};

MessageProducer.prototype.sendMessage = function sendMessage(messageToPublish){
  this._stompClient.publish('csfResult', messageToPublish);
};

module.exports = new MessageProducer();


    //send result to mq server
    // let returnJson = {
    //     "taskId": 'faaa4ce292d74425ae360bb2caccc77f',
    //     "status": "SUCCESS",
    //     "message": '',
    //     "link":'http://140.92.13.107/test.zip'
    // };

  // init();
  // sendMessage(returnJson);