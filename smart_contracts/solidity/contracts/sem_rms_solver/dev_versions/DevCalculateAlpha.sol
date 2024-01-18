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
contract DevCalculateAlpha {

    int INPUT_MULTIPLIER = 1e18;
    uint PRECISION = 18;

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
        // console.logUint(_a1.length);
        // console.logUint(_a2.length);
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

    // Removes maximum number of trailing zeros without effecting ratios across a
    // THIS FUNCTION IS SLIGHTLY WRONG
    // THIS SHOULD SCALE TO NOT REMOVE FINAL PRECISION, SWAP MIN_MULT FOR MAX_MULT MAYBE?
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
        // a[0][0] = a[0][0] + 1;
        return a;
    }

    /// @notice Inverts a given matrix `a` using Gaussian elimination.
    /// @param a The coefficient matrix to be inverted.
    /// @return An array containing the solution vector.
    function solve_matrix(int256[][] memory a) 
        public 
        view 
        returns (int256[] memory) 
    {  
        // a should be input as follows with any required dimensions
        //  | a, a, a, b |
        //  | a, a, a, b |
        //  | a, a, a, b |
        //  | a, a, a, b |
        int256[][] memory a_triangle = _upper_triangular(a);
        int256[] memory x = _back_substitution(a_triangle);
        return x;        
    }


    /// @notice Converts a given matrix `a` into upper triangular form using Gaussian elimination.
    /// @param a The matrix to be transformed.
    /// @return The matrix in upper triangular form.
    function _upper_triangular(int256[][] memory a)
        public 
        view 
        returns (int256[][] memory) 
    {
        // Gets dimensions of array
        uint k = a.length;
        uint k2 = a[0].length;
        // Gets matrix in Echelon Form
        // z - determines the diagnol
        // y - determines the row that the operation is being done on
        // x - determines the column in the row of the operation
        for (uint z = 0; z < k-1; z++) {
            int256[][] memory a2 = new int256[][](k);
            int mul_1 = a[z][z];
            require(mul_1 != 0, "Input matrix is singular");
            // Loop through rows
            for (uint y = 0; y < k; y++) {
                int256[] memory a2_temp = new int256[](k2);
                if (y <= z) {a2_temp = a[y];}
                else {
                    // Loop through columns
                    int mul_2 = a[y][z];
                    require(mul_2 != 0, "Input matrix is singular");
                    // Calculate first value
                    for (uint x = 0; x < k2; x++) {
                        // Guassian Elimination
                        a2_temp[x] = a[y][x]*mul_1 - a[z][x]*mul_2;
                    }
                }
                a2[y] = a2_temp;  
            }
            // REPLACE SCALE ARRAY WITH FUNCTION TO SCALE TO MORE PRECISION
            // COULD SCALE TO 1e36 and REMAIN INSIDE 2^255
            a = scale_array2(a2);
            a = a2;
            
        }
        return a;
    }


    /// @notice Solves a system of equations using backward substitution after Gaussian elimination.
    /// @param a The upper triangular matrix representing the system of equations.
    /// @return An array containing the solution vector.
    function _back_substitution(int256[][] memory a)
        public
        view
        returns (int256[] memory)
    {
        
        uint k = a.length;
        uint k2 = a[0].length;
        // Scales all values to PRECISION
        a = scale_array2(a);
        // print_2array(a);
        int256[] memory out = new int256[](k);
        int256 d;
        for (uint y = k-1; y >= 0; y--) {
            d = scale(a[y][k2-1], PRECISION);

            // Sum up subtraction of already found values
            for (uint x = k-1; x > y; x-- ) {
                d -= (a[y][x]*out[x]);
            }
            // Divide by coefficient of the value to find for that specific row
            out[y] = divide2(d, a[y][y]);
            // End as need to include zero but uint loop cant hit -1
            if (y == 0) {
                break;
            }
        }
        return out;
    }

    /// @notice Divides a number by another number allowing for decimal division
    /// @param a Numerator
    /// @param b Divisor
    /// @return The a divided by b
    function divide (int256 a, int256 b) 
        public
        view
        returns(int256)
    {  
        require(b != 0, "Cant divide by zero");
        int256 a_scaled = scale(a, PRECISION);        
        int256 out = (a_scaled-(a_scaled % b))/b;
        return descale(out, PRECISION);
    }

    /// @notice Divides a number by another number allowing for decimal division
    /// @param a Numerator
    /// @param b Divisor
    /// @return The a divided by b
    function divide2 (int256 a, int256 b) 
        public
        view
        returns(int256)
    {  
        require(b != 0, "Cant divide by zero");     
        int256 out = (a-(a % b))/b;
        return out;
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

    /// @notice Scales a 2d array so that each row has a maximum precision of PRECISION
    /// @param a the array to scale
    /// @return The input array scaled
    function scale_array2 (int256[][] memory a) 
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
                if (max_log < 2*PRECISION) {
                    a[y][x] = scale(a[y][x], (2*PRECISION)-max_log);
                }
                else if (max_log > 2*PRECISION) {
                    a[y][x] = descale(a[y][x], max_log-(2*PRECISION));
                }
                
            }                      
        } 
        return a;
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

    function _compute_alpha_1 (string[][] memory _s_mat, string[] memory _s_b) 
        public
        returns (int256[] memory alpha_)
    {
        // Convert string input to int256
        int256[][] memory _mat = array2dStringToInt(_s_mat);
        int256[] memory _b = array1dStringToInt(_s_b);
    }

    function _compute_alpha_2 (string[][] memory _s_mat, string[] memory _s_b) 
        public
        returns (int256[] memory alpha_)
    {
        // Convert string input to int256
        int256[][] memory _mat = array2dStringToInt(_s_mat);
        int256[] memory _b = array1dStringToInt(_s_b);
        
        // Computes beta matrix from S matrix
        int256[][] memory beta = _compute_beta(_mat);
    }

    function _compute_alpha_3 (string[][] memory _s_mat, string[] memory _s_b) 
        public
        returns (int256[] memory alpha_)
    {
        // Convert string input to int256
        int256[][] memory _mat = array2dStringToInt(_s_mat);
        int256[] memory _b = array1dStringToInt(_s_b);
        
        // Computes beta matrix from S matrix
        int256[][] memory beta = _compute_beta(_mat);
        
        // Appends _b to beta matrix so that it can be solved
        int256[][] memory matrix_to_solve = _append_array(beta, _b);
    }

    function _compute_alpha_4 (string[][] memory _s_mat, string[] memory _s_b) 
        public
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
        // matrix_to_solve = scale_array_small(matrix_to_solve);
        // This is a weird thing that makes it not symettrical
        // This will hopefully be removed in the future
        matrix_to_solve[0][0] += 1;
        // Solve the beta matrix to get alpha_
        alpha_ = solve_matrix(matrix_to_solve);
    }

    function _compute_alpha_5 (string[][] memory _s_mat, string[] memory _s_b) 
        public
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
        // matrix_to_solve = scale_array_small(matrix_to_solve);
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