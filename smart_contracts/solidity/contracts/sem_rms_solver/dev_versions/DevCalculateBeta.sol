// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.9;

import "../../maths/FloatingPointMaths.sol";
import "../../matrix/MatrixMaths.sol";
import "../../generic/IO.sol";

// Dev
import "hardhat/console.sol";


/// @title Calculates Alpha
/// @author 0x365
/// @notice Calculates Alpha from S matrix
/// @dev WIP - currently only square matrices i,j combinations
contract DevCalculateBeta is MatrixMaths, IO {

    int INPUT_MULTIPLIER = 1e18;

    function _compute_beta_seperate (string[][] memory _s_mat)
        public
        returns (int[][] memory)
    {
        console.log("Start");
        // Convert string input to int256
        int256[][] memory _mat = array2dStringToInt(_s_mat);
        return _compute_beta(_mat);
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

}