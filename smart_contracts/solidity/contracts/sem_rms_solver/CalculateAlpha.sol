// ---------- Copyright (C) 2024 University of Strathclyde and Author ---------
// ------------------------- Author: Robert Cowlishaw -------------------------
// -------------- e-mail: robert.cowlishaw.2017@uni.strath.ac.uk --------------

pragma solidity ^0.8.9;

import "../matrix/GuassianSolve.sol";
import "./CalculateBeta.sol";
import "../generic/IO.sol";

// Dev
import "hardhat/console.sol";
import "../generic/DevTools.sol";

/// @title Calculates Alpha
/// @author 0x365
/// @notice Calculates Alpha from S matrix
/// @dev WIP - currently only square matrices i,j combinations
contract CalculateAlpha is CalculateBeta, GuassianSolve, DevTools {

    //int INPUT_MULTIPLIER = 1e14;

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