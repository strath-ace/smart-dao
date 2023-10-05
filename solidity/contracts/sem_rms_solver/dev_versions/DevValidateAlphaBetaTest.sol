// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.9;

import "../CalculateBeta.sol";
import "../../generic/IO.sol";

// Dev
import "hardhat/console.sol";

/// @title Validate Alpha
/// @author 0x365
/// @notice Checks if alpha fits for a given S matrix
/// @dev WIP - needs integrated into other contracts, problems may arise with rounding errors
contract DevValidateAlphaBetaTest is CalculateBeta {
 
    //uint PRECISION = 18;

    // Difference to the power of 10^-PRECISION accepted as validated
    int THRESHOLD = 10000;
    int DECIMAL_THRESHOLD = 10; // Future addition for number of decimals to be accurate too

    function _validate_alpha (string[][] memory _s_mat, string[] memory _s_a) 
        public
        returns (bool)    
    {
        // Convert string input to int256
        int256[][] memory _mat = array2dStringToInt(_s_mat);
        int256[] memory _alpha = array1dStringToInt(_s_a);

        // Computes beta matrix from S matrix
        int256[][] memory _beta = _compute_beta(_mat);

        // Scales array to 1e18
        _beta = scale_array(_beta);

        // Check if everything adds up 
        int256 sum;
        bool success = false;
        for (uint y = 0; y < _beta.length; y++) {
            sum = 0;
            // Sum the row with alpha multiplied
            for (uint x = 0; x < _beta[0].length; x++) {
                sum += _beta[y][x] * _alpha[x];
            }
            if (sum < 0) {
                sum = sum * -1;
            }
            if (sum == 0) {
                success = false;
                return false;
            }
            // Check if sum is small, less than threshold
            if (descale(sum, PRECISION) < THRESHOLD) {
                success = true;
            }
            else {
                success = false;
                return false;
            }
        }
        return success;
    }

    

}