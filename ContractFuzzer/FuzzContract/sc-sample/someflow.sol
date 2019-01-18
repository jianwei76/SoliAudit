contract C {
    // (2**256 - 1) + 1 = 0
    function overflow(uint8 xx) returns (uint8 _overflow) {
        //uint256 max = 2**256 - 1;
        uint8 max = xx;
        return xx +1;
    }

    // 0 - 1 = 2**256 - 1
    function underflow(uint8 xx) returns (uint8 _underflow) {
        uint8 min = xx;
        return min - 1;
    }
}