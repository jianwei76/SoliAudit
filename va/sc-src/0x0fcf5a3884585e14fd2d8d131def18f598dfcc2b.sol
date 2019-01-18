/// @title Token Register Contract
/// @author Kongliang Zhong - <<a href="/cdn-cgi/l/email-protection" class="__cf_email__" data-cfemail="214a4e4f464d48404f46614d4e4e5153484f460f4e5346">[email protected]</a>>,
/// @author Daniel Wang - <<a href="/cdn-cgi/l/email-protection" class="__cf_email__" data-cfemail="3357525d5a565f735f5c5c43415a5d541d5c4154">[email protected]</a>>.
library Bytes32Lib {

    function xorReduce(
        bytes32[]   arr,
        uint        len
        )
        public
        constant
        returns (bytes32 res) {

        res = arr[0];
        for (uint i = 1; i < len; i++) {
            res = _xor(res, arr[i]);
        }
    }

    function _xor(
        bytes32 bs1,
        bytes32 bs2
        )
        public
        constant
        returns (bytes32 res) {

        bytes memory temp = new bytes(32);
        for (uint i = 0; i < 32; i++) {
            temp[i] = bs1[i] ^ bs2[i];
        }
        string memory str = string(temp);
        assembly {
            res := mload(add(str, 32))
        }
    }
}