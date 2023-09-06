// SPDX-License-Identifier: BSD-4-Clause
pragma solidity >=0.8.19;

import "hardhat/console.sol";

/// @title Solidity Development Tools
/// @author 0x365
/// @notice Just some tools for development
/// @dev WIP
contract DevTools {

    /// @notice Prints a 2D array to console
    /// @param a 2D int256 array to be printed
    function print_2array(int256[][] memory a)
        public
        view
    {
        for (uint y = 0; y < a.length; y++) {
            for (uint x = 0; x < a[0].length; x++) {
                console.logInt(a[y][x]);
            }
        }
    }

    /// @notice Prints a 1D array to console
    /// @param a 1D int256 array to be printed
    function print_1array(int256[] memory a)
        public
        view
    {
        for (uint x = 0; x < a.length; x++) {
            console.logInt(a[x]);
        }
    }

}
