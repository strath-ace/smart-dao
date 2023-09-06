const { time, loadFixture, } = require("@nomicfoundation/hardhat-network-helpers");
const { anyValue } = require("@nomicfoundation/hardhat-chai-matchers/withArgs");
const { expect } = require("chai");



describe("EO Data Consensus Contracts", function () {
    // We define a fixture to reuse the same setup in every test.
    // We use loadFixture to run this setup once, snapshot that state,
    // and reset Hardhat Network to that snapshot in every test.
    async function deployBlank() {
        // Contracts are deployed using the first signer/account by default
        const [owner, acc_b, acc_c, acc_d] = await ethers.getSigners();
        const Contract = await ethers.getContractFactory("Blank");
        const app = await Contract.deploy();
        return { app, owner, acc_b, acc_c, acc_d };
    }

     /////////////////////////////////////////////////////////////
     describe("MeasureBlankGas", function () {
        it("Should deploy blank contract", async function () {
            const { app, owner } = await loadFixture(deployBlank);
        });
        it("Should call function in blank contract", async function () {
            // Deploy App
            const { app, owner } = await loadFixture(deployBlank);
            // Run method
            result = await app._say_true();
            // Check result is valid
            expect(await result).to.equal(true);
        });
    });

    
    
    
});
