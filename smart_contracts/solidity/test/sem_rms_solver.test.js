// ---------- Copyright (C) 2024 University of Strathclyde and Author ---------
// ------------------------- Author: Robert Cowlishaw -------------------------
// -------------- e-mail: robert.cowlishaw.2017@uni.strath.ac.uk --------------

const { time, loadFixture, } = require("@nomicfoundation/hardhat-network-helpers");
const { anyValue } = require("@nomicfoundation/hardhat-chai-matchers/withArgs");
const { expect } = require("chai");

// WIP
// Test near misses
// Test just in
// Test far misses

const S_MATRIX_TEST1 = [
    [1, 0.25613333, 0.05081417],
    [0.33729138, 1, 0.03541658],
    [0.52717319, 0.27902039, 1]
]

const S_MATRIX_TEST2 = [
    [1, 0.543, 0.01],
    [0.23, 1, 0.3],
    [0.4, 0.905, 1]
]

// DO 4x4 MATRIX
const S_MATRIX_TEST3 = [
    [1, 0.5439, 0.1235, 0.3972],
    [0.87534, 1, 0.3824, 0.67345],
    [0.123, 0.3223, 1, 0.21673],
    [0.321, 0.423, 0.2, 1]
]

// These values are 10^18 larger than real
const ANSWER_TEST1 = [313271759123458400, 314925909727823360, 371802331148718200];
const ANSWER_TEST2 = [300105279676620000, 314528422925960000, 385366297397410000];
const ANSWER_TEST3 = [251391580000000000, 286427310000000000, 220167520000000000, 242013590000000000]

describe("EO Data Consensus Contracts", function () {
    // We define a fixture to reuse the same setup in every test.
    // We use loadFixture to run this setup once, snapshot that state,
    // and reset Hardhat Network to that snapshot in every test.
    async function deployCalcualteAlpha() {
        // Contracts are deployed using the first signer/account by default
        const [owner, acc_b, acc_c, acc_d] = await ethers.getSigners();
        const Contract = await ethers.getContractFactory("CalculateAlpha");
        const app = await Contract.deploy();
        return { app, owner, acc_b, acc_c, acc_d };
    }

    async function deployValidateAlpha() {
        // Contracts are deployed using the first signer/account by default
        const [owner, acc_b, acc_c, acc_d] = await ethers.getSigners();
        const Contract = await ethers.getContractFactory("ValidateAlphaBetaTest");
        const app = await Contract.deploy();
        return { app, owner, acc_b, acc_c, acc_d };
    }

    async function deployCalculateBeta() {
        // Contracts are deployed using the first signer/account by default
        const [owner, acc_b, acc_c, acc_d] = await ethers.getSigners();
        const Contract = await ethers.getContractFactory("CalculateBeta");
        const app = await Contract.deploy();
        return { app, owner, acc_b, acc_c, acc_d };
    }

    async function deployBlank() {
        // Contracts are deployed using the first signer/account by default
        const [owner, acc_b, acc_c, acc_d] = await ethers.getSigners();
        const Contract = await ethers.getContractFactory("Blank");
        const app = await Contract.deploy();
        return { app, owner, acc_b, acc_c, acc_d };
    }

    /////////////////////////////////////////////////////////////
    describe("Compute Beta", function () {
        it("Should deploy calculate beta", async function () {
            const { app, owner } = await loadFixture(deployCalculateBeta);
        });
        it("Should compute beta for a given S matrix", async function () {
            // Deploy App
            const { app, owner } = await loadFixture(deployCalculateBeta);
            // Multiply S matrix values to remove decimals
            const in_matrix = S_MATRIX_TEST1;
            const DECIMALS = 18
            const multiplier = Math.pow(10, DECIMALS);
            k1 = in_matrix.length;
            k2 = in_matrix[0].length;
            var matrix = []
            var alpha = []
            for (let y = 0; y < k1; y++) {
                var temp = [];
                for (let x = 0; x < k2; x++) {
                    temp.push(String(Math.round((in_matrix[y][x]) * multiplier)));
                }
                matrix.push(temp);
            }
            // Run method, compute beta from S matrix
            result = await app._compute_beta_seperate(matrix);
            // Check result is valid
            // RESULT CHECKER
        });
    });


    /////////////////////////////////////////////////////////////
    describe("CalculateAlphaTest", function () {
        it("Should deploy calculate alpha", async function () {
            const { app, owner } = await loadFixture(deployCalcualteAlpha);
        });
        it("Should calculate alpha from S matrix", async function () {
            // Deploy App
            const { app, owner } = await loadFixture(deployCalcualteAlpha);
            // Multiply S matrix values to remove decimals
            const in_matrix = S_MATRIX_TEST1;
            const DECIMALS = 18
            const multiplier = Math.pow(10, DECIMALS);
            k1 = in_matrix.length;
            k2 = in_matrix[0].length;
            var B = []
            var matrix = []
            for (let y = 0; y < k1; y++) {
                var temp = [];
                for (let x = 0; x < k2; x++) {
                    temp.push(String(Math.round((in_matrix[y][x]) * multiplier)));
                }
                matrix.push(temp);
                B.push(String(multiplier));
            }
            // Run method, compute alpha from S matrix
            result = await app._compute_alpha(matrix, B);
            // Parse Result
            var result_out = [];
            for (let i = 0; i < result.length; i++) {
                result_out[i] = parseInt(result[i]);
            }
            // Check values equal expected alpha values
            // Expected results computed using multiple other methods
            for (let i = 0; i<ANSWER_TEST1.length; i++) {
                var actual = Math.round(await result_out[i]/(multiplier*0.00001))   // Need to fix this
                var theory = Math.round(ANSWER_TEST1[i]/(multiplier*0.00001))
                expect(actual).to.equal(theory);
            }
        });

        it("Should calculate alpha from S matrix 2", async function () {
            // Deploy App
            const { app, owner } = await loadFixture(deployCalcualteAlpha);
            // Multiply S matrix values to remove decimals
            const in_matrix = S_MATRIX_TEST2;
            const DECIMALS = 18
            const multiplier = Math.pow(10, DECIMALS);
            k1 = in_matrix.length;
            k2 = in_matrix[0].length;
            var B = []
            var matrix = []
            for (let y = 0; y < k1; y++) {
                var temp = [];
                for (let x = 0; x < k2; x++) {
                    temp.push(String(Math.round((in_matrix[y][x]) * multiplier)));
                }
                matrix.push(temp);
                B.push(String(multiplier));
            }
            // Run method, compute alpha from S matrix
            result = await app._compute_alpha(matrix, B);
            // Parse Result
            var result_out = [];
            for (let i = 0; i < result.length; i++) {
                result_out[i] = parseInt(result[i]);
            }
            // Check values equal expected alpha values
            // Expected results computed using multiple other methods
            for (let i = 0; i<ANSWER_TEST2.length; i++) {
                var actual = Math.round(await result_out[i]/(multiplier*0.1))   // Need to fix this
                var theory = Math.round(ANSWER_TEST2[i]/(multiplier*0.1))
                expect(actual).to.equal(theory);
            }
        });
        it("Should calculate alpha from S matrix 3", async function () {
            // Deploy App
            const { app, owner } = await loadFixture(deployCalcualteAlpha);
            // Multiply S matrix values to remove decimals
            const in_matrix = S_MATRIX_TEST3;
            const DECIMALS = 18
            const multiplier = Math.pow(10, DECIMALS);
            k1 = in_matrix.length;
            k2 = in_matrix[0].length;
            var B = []
            var matrix = []
            for (let y = 0; y < k1; y++) {
                var temp = [];
                for (let x = 0; x < k2; x++) {
                    temp.push(String(Math.round((in_matrix[y][x]) * multiplier)));
                }
                matrix.push(temp);
                B.push(String(multiplier));
            }
            // Run method, compute alpha from S matrix
            result = await app._compute_alpha(matrix, B);
            // Parse Result
            var result_out = [];
            for (let i = 0; i < result.length; i++) {
                result_out[i] = parseInt(result[i]);
            }
            // Check values equal expected alpha values
            // Expected results computed using multiple other methods
            for (let i = 0; i<ANSWER_TEST3.length; i++) {
                var actual = Math.round(await result_out[i]/(multiplier*0.0001))   // Need to fix this
                var theory = Math.round(ANSWER_TEST3[i]/(multiplier*0.0001))
                expect(actual).to.equal(theory);
            }
        });
    });


    /////////////////////////////////////////////////////////////
    describe("ValidateAlphaTest", function () {
        it("Should deploy validate alpha", async function () {
            const { app, owner } = await loadFixture(deployValidateAlpha);
        });
        it("Should validate alpha for a given S matrix", async function () {
            // Deploy App
            const { app, owner } = await loadFixture(deployValidateAlpha);
            // Multiply S matrix values to remove decimals
            const in_matrix = S_MATRIX_TEST1;
            const DECIMALS = 18
            const multiplier = Math.pow(10, DECIMALS);
            k1 = in_matrix.length;
            k2 = in_matrix[0].length;
            var matrix = []
            var alpha = []
            for (let y = 0; y < k1; y++) {
                var temp = [];
                for (let x = 0; x < k2; x++) {
                    temp.push(String(Math.round((in_matrix[y][x]) * multiplier)));
                }
                matrix.push(temp);
                alpha.push(String(ANSWER_TEST1[y]));
            }
            console.log(matrix);
            console.log(alpha);
            // Run method, compute alpha from S matrix
            result = await app._validate_alpha(matrix, alpha);
            // Check result is valid
            expect(await result).to.equal(true);
        });

        
    });

    
    
    
});