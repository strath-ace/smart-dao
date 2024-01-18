// ---------- Copyright (C) 2024 University of Strathclyde and Author ---------
// ------------------------- Author: Robert Cowlishaw -------------------------
// -------------- e-mail: robert.cowlishaw.2017@uni.strath.ac.uk --------------

pragma solidity ^0.8.19;

import "../maths/FloatingPointMaths.sol";

// Dev
import "hardhat/console.sol";


/// @title Calculates Alpha
/// @author 0x365
/// @notice Calculates Alpha from S matrix
/// @dev WIP - currently only square matrices i,j combinations
contract MatrixMaths is FloatingPointMaths {

    // Sums each row of a 2d matrix
    function _calc_sum_2d_to_1d (int[][] memory _arr) 
        public
        pure
        returns (int[] memory) 
    {
        int[] memory sum_arr_ = new int[](_arr.length);
        for (uint i = 0; i < _arr.length; i++) {
            sum_arr_[i] = _calc_sum_1d_to_0d(_arr[i]);
        }
        return sum_arr_;
    }

    // Sums a 1d matrix
    function _calc_sum_1d_to_0d (int[] memory _arr) 
        public
        pure
        returns (int sum_) 
    {
        for (uint i = 0; i < _arr.length; i++) {
            sum_ += _arr[i];
        }
        return sum_;
    }
    
    // Calculates lamda where lamda is (_mat + transpose(_mat))
    function _add_transpose (int[][] memory _mat) 
        public
        pure
        returns (int[][] memory) 
    {
        uint _size = _mat.length;
        int[][] memory lamda_ = new int[][](_size);
        for (uint j = 0; j < _size; j++) {        
            int[] memory temp = new int[](_size);
            for (uint i = 0; i < _size; i++) {
                temp[i] = (_mat[j][i] + _mat[i][j]); 
            }
            lamda_[j] = temp;
        }
        return lamda_;
    }

    // Scale values so _a sums to 1 { a[i]/sum(a) }
    function _array_sum_to_one (int256[] memory _a) 
        public
        view
        returns (int256[] memory)
    {
        int256 sum = _calc_sum_1d_to_0d(_a);
        int256[] memory a_ = new int256[](_a.length);
        for (uint x = 0; x < _a.length; x++) {
            a_[x] = divide(scale(_a[x], PRECISION), sum);
        }
        return a_;
    }

    // Joins two arrays together (2d and 1d)
    function _append_array (int256[][] memory _a1, int256[] memory _a2)
        public
        view
        returns (int256[][] memory)
    {
        console.logUint(_a1.length);
        console.logUint(_a2.length);
        // Create variables
        int256[] memory temp;
        int256[][] memory join_array_ = new int256[][](_a2.length);
        // Joins arrays together
        for (uint i = 0; i < _a1.length; i++) {
            temp = new int256[](_a1[0].length+1);
            for (uint x = 0; x < _a1[0].length; x++) {
                temp[x] = _a1[i][x];
            }
            temp[_a1[0].length] = _a2[i];
            join_array_[i] = temp;
        }
        return join_array_;
    }

}