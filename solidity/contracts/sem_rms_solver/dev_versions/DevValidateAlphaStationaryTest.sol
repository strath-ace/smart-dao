// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.9;

// Dev
import "hardhat/console.sol";
//import "./library/Tools.sol";

/// @title Validate Alpha
/// @author 0x365
/// @notice Checks if alpha fits for a given S matrix
/// @dev WIP - needs integrated into other contracts, problems may arise with rounding errors
contract DevValidateAlphaStationaryTest {

    // Convert 2d string array to 2d int256 array
    function array2dStringToInt (string[][] memory s) 
        public
        pure
        returns (int256[][] memory)
    {
        uint8 k = uint8(s.length);
        int256[][] memory result = new int256[][](k);
        for (uint8 i = 0; i < k; i++) {
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
        uint8 k = uint8(s.length);
        int256[] memory result = new int256[](k);
        for (uint8 i = 0; i <k; i++) {
            result[i] = stringToInt(s[i]);
        }
        return result;
    }

    // Converts string to int256
    function stringToInt (string memory s) 
        internal
        pure
        returns (int) 
    {
        bytes memory b = bytes(s);
        int256 result = 0;
        for (uint i = 0; i < b.length; i++) {
            uint8 c = (uint8(b[i]));
            if (c >= 48 && c <= 57) {
                result = result * 10 + (int256(uint256(c)) - 48);
            }
        }
        return result;
    }

    function rms(int256[][] memory _s, int256[] memory _a)
        public
        view
        returns (int)
    {
        uint k = uint(_a.length);
        int g_f = 0;
        int h_f = 0;
        for (uint i = 0; i < k; i++) {
            for (uint j = 0; j < k; j++) {
                g_f += (1e18-_s[i][j])*_a[i]*_a[i];
                h_f += (_s[i][j])*(_a[i]-_a[j])*(_a[i]-_a[j]);
            }
        }
        return (g_f+h_f)/1e36;
    }

    function _validate_alpha (string[][] memory _s_mat, string[] memory _s_a)
        public
        returns (bool)
    {
        // Convert string input to int256
        int256[][] memory _mat = array2dStringToInt(_s_mat);
        int256[] memory _a = array1dStringToInt(_s_a);

        uint k = (_a.length);

        require(k >= 3, "Matrix too small");

        // Check around optimal value
        int opt_rms = rms(_mat, _a);
        int test_val;
        for (uint i = 0; i < k; i++) {
            _a[i] += 1;
            for (uint j = 0; j < k; j++) {
                if (i != j) {
                    _a[j] += 1;
                    test_val = rms(_mat, _a);
                    require(test_val >= opt_rms, "Not optimal value");
                    _a[j] -= 1;
                }
            }
            _a[i] -= 1;
        }
        return true;
    }
}