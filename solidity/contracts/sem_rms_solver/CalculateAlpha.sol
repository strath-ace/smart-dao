// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.9;

// import "../matrix/GuassianSolve.sol";
// import "./CalculateBeta.sol";
// import "../generic/IO.sol";

// Dev
import "hardhat/console.sol";

/// @title Calculates Alpha
/// @author 0x365
/// @notice Calculates Alpha from S matrix
/// @dev WIP - currently only square matrices i,j combinations
contract CalculateAlpha {

    int INPUT_MULTIPLIER = 1e18;

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

    // Builds list combinations of i and j values for building coefficients
    function _build_i_j_list (uint256 k) 
        public
        view
        returns (uint256[] memory, uint256[] memory)
    {
        uint quant = (k * (k-1))/2;
        uint256[] memory out_i = new uint256[](k);
        uint256[] memory out_j = new uint256[](k);
        uint256 x = 0;
        uint256 y = 1;
        uint256 ii = 0;
        while (ii < k) {
            out_i[ii] = x;
            out_j[ii] = y;
            y++;
            if (y == k) {
                x++;
                y = x + 1;
            }
            ii++;
        }
        return (out_i, out_j);
    }

    //  Computes Beta matrix from S matrix
    function _compute_beta (int[][] memory _mat) 
        public
        view
        returns (int[][] memory)
    {
        uint k = _mat[0].length;
        require(k >= 3, "Matrix must be size 3 or larger");
        // Caculates variables required to calculate beta values
        int[][] memory _lamda = _add_transpose(_mat);
        int[] memory _sum_mat = _calc_sum_2d_to_1d(_mat);
        int[] memory _sum_lamda = _calc_sum_2d_to_1d(_lamda);
        // Gets unique combinations of i and j for beta
        (uint[] memory i_li, uint[] memory j_li) = _build_i_j_list(k);
        // Create empty array
        int[][] memory beta_array = new int[][](i_li.length); 
        // Get correctly scaled constants
        int k_val = int(k) * INPUT_MULTIPLIER;
        int minus2 = int(2) * INPUT_MULTIPLIER;
        // Compute beta for each unique i,j combination
        for (uint y = 0; y < k; y++) {
            int[] memory beta_list = new int[](k);
            uint i = i_li[y];
            uint j = j_li[y];
            for (uint x = 0; x < k; x++) {
                if (x == i) {
                    beta_list[x] = k_val - _sum_mat[i] + _sum_lamda[i] - minus2 + _lamda[j][i];
                }
                else if (x == j) {
                    beta_list[x] =_sum_mat[j] - k_val + minus2 - _sum_lamda[j] - _lamda[i][j];
                }
                else {
                    beta_list[x] = _lamda[j][x] - _lamda[i][x];
                }
            }
            beta_array[y] = beta_list;
        }
        return (beta_array);
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

    function _compute_alpha (string[][] memory _s_mat, string[] memory _s_b) 
        public
        view
        returns (int256[] memory alpha_)
    {
        // Convert string input to int256
        int256[][] memory _mat = array2dStringToInt(_s_mat);
        int256[] memory _b = array1dStringToInt(_s_b);
        // Computes beta matrix from S matrix
        int256[][] memory beta = _compute_beta(_mat);
        // Appends _b to beta matrix so that it can be solved
        int256[][] memory matrix_to_solve = _append_array(beta, _b);
        // Shrinks matrix_to_solve to minimum size without loosing accuracy
        matrix_to_solve = scale_array_small(matrix_to_solve);
        // This is a weird thing that makes it not symettrical
        // This will hopefully be removed in the future
        matrix_to_solve[0][0] += 1;
        // Solve the beta matrix to get alpha_
        alpha_ = solve_matrix(matrix_to_solve);
        // Scale values so alpha_ sums to 1
        alpha_ = _array_sum_to_one(alpha_);
        // Return alpha_
        return alpha_;
    }

}