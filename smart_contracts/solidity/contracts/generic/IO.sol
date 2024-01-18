// ---------- Copyright (C) 2024 University of Strathclyde and Author ---------
// ------------------------- Author: Robert Cowlishaw -------------------------
// -------------- e-mail: robert.cowlishaw.2017@uni.strath.ac.uk --------------

pragma solidity ^0.8.19;

// Dev
import "hardhat/console.sol";
//import "DevTools.sol";

/// @title Input Output (IO)
/// @author 0x365
/// @notice Useful functions for input and output
/// @dev WIP
contract IO {

    // Convert 2d string array to 2d int256 array
    function array2dStringToInt (string[][] memory s) 
        public
        pure
        returns (int256[][] memory)
    {
        int256[][] memory result = new int256[][](s.length);
        for (uint i = 0; i < s.length; i++) {
            result[i] = array1dStringToInt(s[i]);
        }
        return result;
    }

    // Convert 1d string array to 1d int256 array
    function array1dStringToInt (string[] memory s) 
        public
        pure
        returns (int256[] memory)    
    {
        int256[] memory result = new int256[](s.length);
        for (uint i = 0; i < s.length; i++) {
            result[i] = stringToInt(s[i]);
        }
        return result;
    }

    // Converts string to int256
    function stringToInt (string memory s) 
        public
        pure
        returns (int) 
    {
        bytes memory b = bytes(s);
        int result = 0;
        for (uint i = 0; i < b.length; i++) {
            int256 c = int256(int8(uint8(b[i])));
            if (c >= 48 && c <= 57) {
                result = result * 10 + (c - 48);
            }
        }
        return result;
    }

    // Converts int256 to string
    // function intToString (int256 num) 
    //     public
    //     view
    //     returns (string memory)
    // {
    //     string memory result = "";
    //     return result;
    // }
    
    // Converts string to uint256
    function stringToUint (string memory s)
        public
        pure
        returns (uint)
    {
        bytes memory b = bytes(s);
        uint result = 0;
        for (uint i = 0; i < b.length; i++) {
            uint256 c = uint256(uint8(b[i]));
            if (c >= 48 && c <= 57) {
                result = result * 10 + (c - 48);
            }
        }
        return result;
    }

    // Converts uint256 to string
    // function uintToString (uint256 num)
    //     public
    //     view
    //     returns (string memory)
    // {
    //     string memory result = "";
    //     return result;
    // }

}