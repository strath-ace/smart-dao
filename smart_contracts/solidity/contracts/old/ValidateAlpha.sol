// // SPDX-License-Identifier: UNLICENSED
// pragma solidity ^0.8.9;

// // Dev
// import "hardhat/console.sol";
// //import "./library/Tools.sol";

// /// @title Validate Alpha
// /// @author 0x365
// /// @notice Checks if alpha fits for a given S matrix
// /// @dev WIP - needs integrated into other contracts, problems may arise with rounding errors
// contract ValidateAlpha {

//     int256 PRECISION = 1e18;
//     int256 THRESHOLD_PRECISION = 1e2;
//     int256 CALCULATED_PRECISION = PRECISION/THRESHOLD_PRECISION;

//     function _calc_sum_2d_to_1d (int[][] memory _arr) 
//         internal
//         pure
//         returns (int[] memory) 
//     {
//         int[] memory sum_arr_ = new int[](_arr.length);
//         for (uint i = 0; i < _arr.length; i++) {
//             sum_arr_[i] = _calc_sum_1d_to_0d(_arr[i]);
//         }
//         return sum_arr_;
//     }

//     // Sums a 1d matrix
//     function _calc_sum_1d_to_0d (int[] memory _arr) 
//         public
//         pure
//         returns (int sum_) 
//     {
//         for (uint i = 0; i < _arr.length; i++) {
//             sum_ += _arr[i];
//         }
//         return sum_;
//     }

//     // Convert 2d string array to 2d int256 array
//     function array2dStringToInt (string[][] memory s) 
//         public
//         pure
//         returns (int256[][] memory)
//     {
//         uint8 k = uint8(s.length);
//         int256[][] memory result = new int256[][](k);
//         for (uint8 i = 0; i < k; i++) {
//             result[i] = array1dStringToInt(s[i]);
//         }
//         return result;
//     }

//     // Convert 1d string array to 1d int256 array
//     function array1dStringToInt (string[] memory s) 
//         public
//         pure
//         returns (int256[] memory)    
//     {
//         uint8 k = uint8(s.length);
//         int256[] memory result = new int256[](k);
//         for (uint8 i = 0; i <k; i++) {
//             result[i] = stringToInt(s[i]);
//         }
//         return result;
//     }

//     // Converts string to int256
//     function stringToInt (string memory s) 
//         internal
//         pure
//         returns (int) 
//     {
//         bytes memory b = bytes(s);
//         int256 result = 0;
//         for (uint i = 0; i < b.length; i++) {
//             uint8 c = (uint8(b[i]));
//             if (c >= 48 && c <= 57) {
//                 result = result * 10 + (int256(uint256(c)) - 48);
//             }
//         }
//         return result;
//     }

//     /// @notice Scales a 2d array so that each row has a maximum precision of PRECISION
//     /// @param a the array to scale
//     /// @return The input array scaled
//     function scale_val (int256 a) 
//         public
//         view
//         returns (int256)
//     {
//         uint256 log_val = log10(a);
//         uint256 PREC = log10(PRECISION);
//         // Scales to make the maximum == PRECISION
//         if (log_val < PREC) {
//             a = scale(a, PREC-log_val);
//         }
//         else if (log_val > PREC) {
//             a = descale(a, log_val-PREC);
//         }                    
//         return a;
//     }

//     /// @notice Finds the log10 of a number, ignores negatives
//     /// @param x the number to find the log10 of
//     /// @return The log10 of x
//     function log10 (int256 x) 
//         public
//         pure
//         returns(uint)
//     {
//         // Makes number positive no matter the input
//         if (x < 0) {
//             x = x * -1;
//         }
//         uint counter = 0;
//         // Counts the number of times it can divide by 10 
//         // before the number disappears due to integers only
//         while (x/10 > 0) {
//             counter++;
//             x = x/10;
//         }
//         return counter;
//     }

//     /// @notice Scales a number by an exponent
//     /// @param x the number to scale
//     /// @param scaler the exponent
//     /// @return The value of x*(10^scaler)
//     function scale (int256 x, uint256 scaler) 
//         public
//         pure
//         returns (int256)
//     {
//         int256 base = 10;
//         x = x*(base**scaler);
//         return x;
//     }

//     /// @notice Reduces/Descales a number by an exponent
//     /// @param x the number to reduce
//     /// @param scaler the exponent
//     /// @return The value of x/(10^scaler)
//     function descale (int256 x, uint256 scaler) 
//         public
//         pure
//         returns (int256)
//     {
//         int256 base = 10;
//         x = x/(base**scaler);
//         return x;
//     }

//     // Calculates lamda where lamda is (_mat + transpose(_mat))
//     function _transpose (int[][] memory _mat) 
//         public
//         pure
//         returns (int[][] memory) 
//     {
//         uint _size = _mat.length;
//         int[][] memory lamda_ = new int[][](_size);
//         for (uint j = 0; j < _size; j++) {        
//             int[] memory temp = new int[](_size);
//             for (uint i = 0; i < _size; i++) {
//                 temp[i] = _mat[j][i];
//             }
//             lamda_[j] = temp;
//         }
//         return lamda_;
//     }

//     function _validate_alpha (string[][] memory _s_mat, string[] memory _s_a)
//         public
//         view
//         returns (bool)
//     {
//         // Convert string input to int256
//         int256[][] memory _mat = array2dStringToInt(_s_mat);
//         int256[] memory _a = array1dStringToInt(_s_a);
//         // Check matrix is correct size
//         int256 k = int256(_a.length);
//         uint8 k_len = uint8(int8(k));

//         require(k_len >= 3, "Matrix too small");
//         // Sums each row of a 2d matrix
//         _mat = _transpose(_mat);
//         int[] memory _sum_mat = _calc_sum_2d_to_1d(_mat);
//         // Compute first
//         int256 f;
//         f = _a[0]*_a[0]*(k*1e18-_sum_mat[0]);
//         for (uint8 j = 0; j < k_len; j++) {
//             f += _mat[0][j] * (_a[0] - _a[j]) * (_a[0] - _a[j]);
//         }
//         // THIS MIGHT CAUSE ISSUES WITH alpha=0.001342974
//         f = scale_val(f);
//         console.logInt(f);
//         f = (f-(f%CALCULATED_PRECISION))/CALCULATED_PRECISION;
//         console.logInt(f);
//         // Make sure all others equal the firsts
//         int256 f2;
//         for (uint8 i = 1; i < k_len; i++) {
//             f2 = _a[i]*_a[i]*(k*1e18-_sum_mat[i]);
//             for (uint8 j = 0; j < k_len; j++) {
//                 f2 += _mat[i][j] * (_a[i] - _a[j]) * (_a[i] - _a[j]);
//             }
//             f2 = scale_val(f2);
//             console.logInt(f2);
//             f2 = (f2-(f%CALCULATED_PRECISION))/CALCULATED_PRECISION;
//             console.logInt(f2);
//             require(f2 == f, "Validation Fail");
//         }
//         return true;
//     }
// }