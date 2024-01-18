// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.9;

// Dev
//import "./library/hardhat/console.sol";
//import "./library/Tools.sol";


/// @title Overall design
/// @author 0x365
/// @notice
/// @dev WIP
contract InformationConsensus {

    // struct Notification {
    //     address creator;
    //     uint times_out;
    // }    

    

    // USER MAKES CALL FOR DATA (Could include money bid)

    // USERS PROVIDE DATA (to IPFS?)
    // Somehow need to provide S matrix rather than data itself

    // Someone provides comparison of ipfs data points to generate S matrix
    // Many people do this to find consensus on S matrices

    // Calculate alpha from S matrix inputs

    // Validate alpha from S matrices

}





// uint public unlockTime;
// address payable public owner;

// event Withdrawal(uint amount, uint when);

// constructor(uint _unlockTime) payable {
//     require(
//         block.timestamp < _unlockTime,
//         "Unlock time should be in the future"
//     );

//     unlockTime = _unlockTime;
//     owner = payable(msg.sender);
// }

// function withdraw() public {
    // // Uncomment this line, and the import of "hardhat/console.sol", to print a log in your terminal
    // console.log("Unlock time is %o and block timestamp is %o", unlockTime, block.timestamp);

    // require(block.timestamp >= unlockTime, "You can't withdraw yet");
    // require(msg.sender == owner, "You aren't the owner");

    // emit Withdrawal(address(this).balance, block.timestamp);

    // owner.transfer(address(this).balance);
// }