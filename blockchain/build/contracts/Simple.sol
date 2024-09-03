pragma solidity ^0.8.0;

contract SimpleContract {
    string public test;

    function setTest(string memory _test) public {
        test = _test;
    }
}
