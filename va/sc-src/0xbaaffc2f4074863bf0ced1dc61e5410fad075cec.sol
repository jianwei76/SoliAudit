// sendlimiter
// limit funds held on a contract
// @authors:
// Cody Burns <<a href="/cdn-cgi/l/email-protection" class="__cf_email__" data-cfemail="7f1b10110b0f1e11161c3f1c101b06081d0a0d110c511c1012">[email protected]</a>>
// license: Apache 2.0
// version:

pragma solidity ^0.4.19;

// Intended use:  
// cross deploy to limit funds on a chin identifier
// Status: functional
// still needs:
// submit pr and issues to https://github.com/realcodywburns/
//version 0.1.0


contract sendlimiter{
 function () public payable {
     require(this.balance + msg.value < 100000000);}
}