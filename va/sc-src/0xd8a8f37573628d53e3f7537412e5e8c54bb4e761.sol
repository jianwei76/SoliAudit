/// @title Token Register Contract
/// @author Daniel Wang - <<a href="/cdn-cgi/l/email-protection" class="__cf_email__" data-cfemail="8de9ece3e4e8e1cde1e2e2fdffe4e3eaa3e2ffea">[email protected]</a>>.
library ErrorLib {

    event Error(string message);

    /// @dev Check if condition hold, if not, log an exception and revert.
    function orThrow(bool condition, string message) public constant {
        if (!condition) {
            error(message);
        }
    }

    function error(string message) public constant {
        Error(message);
        revert();
    }
}