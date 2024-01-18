// SPDX-License-Identifier: BSD-4-Clause
pragma solidity >=0.8.19;

// Dev
import "hardhat/console.sol";

/// @title Float Point Maths
/// @author 0x365
/// @notice Some operations for doing maths that may end in decimals
/// @dev WIP
contract FloatingPointMaths {

    uint PRECISION = 18;

    /// @notice Divides a number by another number allowing for decimal division
    /// @param a Numerator
    /// @param b Divisor
    /// @return The a divided by b
    function divide (int256 a, int256 b) 
        public
        view
        returns(int256)
    {  
        int256 a_scaled = scale(a, PRECISION);        
        int256 out = (a_scaled-(a_scaled % b))/b;
        return descale(out, PRECISION);
    }

    /// @notice Finds the log10 of a number, ignores negatives
    /// @param x the number to find the log10 of
    /// @return The log10 of x
    function log10 (int256 x) 
        public
        pure
        returns(uint)
    {
        // Makes number positive no matter the input
        if (x < 0) {
            x = x * -1;
        }
        uint counter = 0;
        // Counts the number of times it can divide by 10 
        // before the number disappears due to integers only
        while (x/10 > 0) {
            counter++;
            x = x/10;
        }
        return counter;
    }


    /// @notice Scales a number by an exponent
    /// @param x the number to scale
    /// @param scaler the exponent
    /// @return The value of x*(10^scaler)
    function scale (int256 x, uint256 scaler) 
        public
        pure
        returns (int256)
    {
        int256 base = 10;
        x = x*(base**scaler);
        return x;
    }

    /// @notice Reduces/Descales a number by an exponent
    /// @param x the number to reduce
    /// @param scaler the exponent
    /// @return The value of x/(10^scaler)
    function descale (int256 x, uint256 scaler) 
        public
        pure
        returns (int256)
    {
        int256 base = 10;
        x = x/(base**scaler);
        return x;
    }


    /// @notice Scales a 2d array so that each row has a maximum precision of PRECISION
    /// @param a the array to scale
    /// @return The input array scaled
    function scale_array (int256[][] memory a) 
        public
        view
        returns (int256[][] memory)
    {
        uint max_log;
        for (uint y = 0; y < a.length; y++) {
            // Finds the maximum log value for each row
            max_log = 0;
            for (uint x = 0; x < a[0].length; x++) {
                if (log10(a[y][x]) > max_log) {
                    max_log = log10(a[y][x]);
                }
            }
            // Scales to make the maximum == PRECISION
            for (uint x = 0; x < a[0].length; x++) {
                if (max_log < PRECISION) {
                    a[y][x] = scale(a[y][x], PRECISION-max_log);
                }
                else if (max_log > PRECISION) {
                    a[y][x] = descale(a[y][x], max_log-PRECISION);
                }
                
            }                      
        } 
        return a;
    }

    // Removes maximum number of trailing zeros without effecting ratios across a
    function scale_array_small (int256[][] memory a) 
        public
        view
        returns (int256[][] memory)
    {
        // Remove any random numbers at end of number
        for (uint y = 0; y < a.length; y++) {
            for (uint x = 0; x < a[0].length; x++) {
                a[y][x] = a[y][x] / 1000;
            }
        }
        // Remove as many trailing zeros as possible
        for (uint y = 0; y < a.length; y++) {
            int256 min_mult = 1e18;
            for (uint x = 0; x < a[0].length; x++) {
                int256 mult = 1;
                while (a[y][x] % mult == 0) {
                    mult = mult * 10;
                }
                if (mult < min_mult) {
                    min_mult = mult;
                }
            }
            for (uint x = 0; x < a[0].length; x++) {
                a[y][x] = a[y][x]/min_mult;
            }
        }
        a[0][0] = a[0][0] + 1;
        return a;
    }

}
