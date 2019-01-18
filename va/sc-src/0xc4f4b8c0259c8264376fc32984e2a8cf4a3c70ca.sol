pragma solidity ^0.4.15;


/// @title Abstract oracle contract - Functions to be implemented by oracles
contract Oracle {

    function isOutcomeSet() public constant returns (bool);
    function getOutcome() public constant returns (int);
}



/// @title Centralized oracle contract - Allows the contract owner to set an outcome
/// @author Stefan George - <<a href="/cdn-cgi/l/email-protection" class="__cf_email__" data-cfemail="e89b9c8d8e8986a88f86879b819bc69885">[email protected]</a>>
contract CentralizedOracle is Oracle {

    /*
     *  Events
     */
    event OwnerReplacement(address indexed newOwner);
    event OutcomeAssignment(int outcome);

    /*
     *  Storage
     */
    address public owner;
    bytes public ipfsHash;
    bool public isSet;
    int public outcome;

    /*
     *  Modifiers
     */
    modifier isOwner () {
        // Only owner is allowed to proceed
        require(msg.sender == owner);
        _;
    }

    /*
     *  Public functions
     */
    /// @dev Constructor sets owner address and IPFS hash
    /// @param _ipfsHash Hash identifying off chain event description
    function CentralizedOracle(address _owner, bytes _ipfsHash)
        public
    {
        // Description hash cannot be null
        require(_ipfsHash.length == 46);
        owner = _owner;
        ipfsHash = _ipfsHash;
    }

    /// @dev Replaces owner
    /// @param newOwner New owner
    function replaceOwner(address newOwner)
        public
        isOwner
    {
        // Result is not set yet
        require(!isSet);
        owner = newOwner;
        OwnerReplacement(newOwner);
    }

    /// @dev Sets event outcome
    /// @param _outcome Event outcome
    function setOutcome(int _outcome)
        public
        isOwner
    {
        // Result is not set yet
        require(!isSet);
        isSet = true;
        outcome = _outcome;
        OutcomeAssignment(_outcome);
    }

    /// @dev Returns if winning outcome is set
    /// @return Is outcome set?
    function isOutcomeSet()
        public
        constant
        returns (bool)
    {
        return isSet;
    }

    /// @dev Returns outcome
    /// @return Outcome
    function getOutcome()
        public
        constant
        returns (int)
    {
        return outcome;
    }
}



/// @title Centralized oracle factory contract - Allows to create centralized oracle contracts
/// @author Stefan George - <<a href="/cdn-cgi/l/email-protection" class="__cf_email__" data-cfemail="c6b5b2a3a0a7a886a1a8a9b5afb5e8b6ab">[email protected]</a>>
contract CentralizedOracleFactory {

    /*
     *  Events
     */
    event CentralizedOracleCreation(address indexed creator, CentralizedOracle centralizedOracle, bytes ipfsHash);

    /*
     *  Public functions
     */
    /// @dev Creates a new centralized oracle contract
    /// @param ipfsHash Hash identifying off chain event description
    /// @return Oracle contract
    function createCentralizedOracle(bytes ipfsHash)
        public
        returns (CentralizedOracle centralizedOracle)
    {
        centralizedOracle = new CentralizedOracle(msg.sender, ipfsHash);
        CentralizedOracleCreation(msg.sender, centralizedOracle, ipfsHash);
    }
}