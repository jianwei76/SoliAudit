/// @title Token Register Contract
/// @author Kongliang Zhong - <<a href="/cdn-cgi/l/email-protection" class="__cf_email__" data-cfemail="dfb4b0b1b8b3b6beb1b89fb3b0b0afadb6b1b8f1b0adb8">[email protected]</a>>,
/// @author Daniel Wang - <<a href="/cdn-cgi/l/email-protection" class="__cf_email__" data-cfemail="debabfb0b7bbb29eb2b1b1aeacb7b0b9f0b1acb9">[email protected]</a>>.
library Uint8Lib {
    function xorReduce(
        uint8[] arr,
        uint    len
        )
        public
        constant
        returns (uint8 res) {

        res = arr[0];
        for (uint i = 1; i < len; i++) {
           res ^= arr[i];
        }
    }
}