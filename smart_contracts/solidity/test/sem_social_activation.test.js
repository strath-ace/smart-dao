// ---------- Copyright (C) 2024 University of Strathclyde and Author ---------
// ------------------------- Author: Robert Cowlishaw -------------------------
// -------------- e-mail: robert.cowlishaw.2017@uni.strath.ac.uk --------------

const { time, loadFixture,} = require("@nomicfoundation/hardhat-network-helpers");
const { anyValue } = require("@nomicfoundation/hardhat-chai-matchers/withArgs");
const { expect } = require("chai");

// Values for a normal notification to be used by test
const notification_reg = {
    in_regions: [435, 436, 437],
    in_type: 2,
    tx_params: {
        gasLimit: 1000000
    },
}


describe("SocialActivation Contract", function () {
    // We define a fixture to reuse the same setup in every test.
    // We use loadFixture to run this setup once, snapshot that state,
    // and reset Hardhat Network to that snapshot in every test.
    async function deploySocialActivation() {
  
        // Contracts are deployed using the first signer/account by default
        const [owner, acc_b, acc_c, acc_d] = await ethers.getSigners();

        // console.log("Account Address'");
        // console.log("Owner: ", owner.address);
        // console.log("Acc_b: ", acc_b.address);
        // console.log("Acc_c: ", acc_c.address);
    
        const Contract = await ethers.getContractFactory("SocialActivation");
        const app = await Contract.deploy();
  
        return { app, owner, acc_b, acc_c, acc_d };
    }


    // ###########################################################################
    describe("Testing parameters okay?", function () {
        it("Should have testing parameters fit in max_region and num_disaster_type parameters", async function () {
            const { app, owner } = await loadFixture(deploySocialActivation);
            threshold = parseInt(await app.THRESHOLD());
            timeout = parseInt(await app.TIMEOUT());
            max_region = parseInt(await app.MAX_REGION());
            num_disaster_types = parseInt(await app.NUM_DISASTER_TYPES());
            expect(threshold).to.be.above(0, "THRESHOLD value in contract must be more than 0");
            expect(timeout).to.be.above(0, "TIMEOUT value in contract must be more than 0");
            for (let i=0; i < notification_reg.in_regions.length; i++) {
                expect(max_region).to.be.above(notification_reg.in_regions[i], "Values for region in test are more than that in MAX_REGION in contract");
            }
            expect(num_disaster_types).to.be.above(-1);
        });
    });

    
    // ###########################################################################
    describe("Deploy Contract", function () {
        it("Should set deployer to authorised user", async function () {
            const { app, owner } = await loadFixture(deploySocialActivation);
            expect(await app.get_authorised(owner.address)).to.equal(true);
        });
        it("Should set deployer to num_notifications to 1", async function () {
            const { app, owner } = await loadFixture(deploySocialActivation);
            expect(await app.num_notifications(owner.address)).to.equal(1);
        });
        it("Should set deployer to num_correct_notifications to 1", async function () {
            const { app, owner } = await loadFixture(deploySocialActivation);
            expect(await app.num_correct_notifications(owner.address)).to.equal(1);
        });
    });


    // ###########################################################################
    describe("Authorise New Users", function () {
        it("Should be deployed with only owner being authorised by default", async function () {
            const { app, owner, acc_b, acc_c } = await loadFixture(deploySocialActivation);
            expect(await app.get_authorised(owner.address)).to.equal(true);
            expect(await app.get_authorised(acc_b.address)).to.equal(false);
            expect(await app.get_authorised(acc_c.address)).to.equal(false);
        });
        it("Should allow authorised users to authorise non-authorised user", async function () {
            const { app, owner, acc_b, acc_c } = await loadFixture(deploySocialActivation);
            expect(await app.get_authorised(owner.address)).to.equal(true);
            expect(await app.get_authorised(acc_b.address)).to.equal(false);
            await app.connect(owner)._authorise_user(acc_b.address);
            expect(await app.get_authorised(owner.address)).to.equal(true);
            expect(await app.get_authorised(acc_b.address)).to.equal(true);
        });
        it("Should not allow non-authorised user to authorise a non-authorised user", async function () {
            const { app, owner, acc_b, acc_c } = await loadFixture(deploySocialActivation);
            expect(await app.get_authorised(acc_b.address)).to.equal(false);
            expect(await app.get_authorised(acc_c.address)).to.equal(false);
            await expect(app.connect(acc_b)._authorise_user(acc_c.address, {gasLimit: 1000000})).to.be.revertedWith("Only authorised users can authorise new users");
            expect(await app.get_authorised(acc_b.address)).to.equal(false);
            expect(await app.get_authorised(acc_c.address)).to.equal(false);
        });
        it("Should not allow re-authoirsation of a user", async function () {
            const { app, owner, acc_b, acc_c } = await loadFixture(deploySocialActivation);
            expect(await app.get_authorised(acc_b.address)).to.equal(false);
            await expect(app.connect(owner)._authorise_user(acc_b.address, {gasLimit: 1000000})).to.not.be.reverted;
            expect(await app.get_authorised(acc_b.address)).to.equal(true);
            await expect(app.connect(owner)._authorise_user(acc_b.address, {gasLimit: 1000000})).to.be.revertedWith("New user is already authorised");
            expect(await app.get_authorised(acc_b.address)).to.equal(true);
        });

    });


    // ###########################################################################
    describe("New Notification Mechanism", function () {
        it("Should not allow non-authorised users", async function () {
            // Deploy Contract
            const { app, owner, acc_b, acc_c } = await loadFixture(deploySocialActivation);
            // Make new notification with acc_b
            tx = app.connect(acc_b)._new_notification(notification_reg.in_regions, notification_reg.in_type, notification_reg.tx_params);
            // Expect Failure
            await expect(tx).to.be.revertedWith("User is not authorised");
        });
        it("Should not allow unknown value for type of disaster", async function () {
            // Deploy Contract
            const { app, owner, acc_b, acc_c } = await loadFixture(deploySocialActivation);
            // Authorise acc_b
            await app.connect(owner)._authorise_user(acc_b.address);
            // Get value of threshold defined in smart contract
            threshold = await app.NUM_DISASTER_TYPES();
            // Make new notification with acc_b
            tx = app.connect(acc_b)._new_notification(notification_reg.in_regions, threshold+1, notification_reg.tx_params);
            // Expect Failure
            await expect(tx).to.be.revertedWith("Not a classified type of disaster (0-5)");
        });
        it("Should not allow value for region outside of boundary", async function () {
            // Deploy Contract
            const { app, owner, acc_b, acc_c } = await loadFixture(deploySocialActivation);
            // Authorise acc_b
            await app.connect(owner)._authorise_user(acc_b.address);
            // Get value of threshold defined in smart contract
            max_region = await app.MAX_REGION();
            // Make new notification with acc_b
            tx = app.connect(acc_b)._new_notification([max_region+1, max_region+10], notification_reg.in_type, notification_reg.tx_params);
            // Expect Failure
            await expect(tx).to.be.revertedWith("Region is outside maximum value");
        });
        it("Should be successfull with authorised user, known type of disaster in region boundary", async function () {
            // Deploy Contract
            const { app, owner, acc_b, acc_c } = await loadFixture(deploySocialActivation);
            // Authorise acc_b
            await app.connect(owner)._authorise_user(acc_b.address);
            // Make new notification with acc_b
            tx = app.connect(acc_b)._new_notification(notification_reg.in_regions, notification_reg.in_type, notification_reg.tx_params);
            // Expect Success
            await expect(tx).not.to.be.reverted;
        });
        it("Should update number of notifications by user", async function () {
            // Deploy Contract
            const { app, owner, acc_b, acc_c } = await loadFixture(deploySocialActivation);
            // Authorise acc_b
            await app.connect(owner)._authorise_user(acc_b.address);
            start_num = parseInt(await app.num_notifications(acc_b.address));
            // Make new notification with acc_b
            await app.connect(acc_b)._new_notification(notification_reg.in_regions, notification_reg.in_type, notification_reg.tx_params);
            // Expect number of notifications to increase to 3
            expect(await app.num_notifications(acc_b.address)).to.equal(start_num+notification_reg.in_regions.length);
        });
        it("Should update user saved timestamps", async function () {
            // Deploy Contract
            const { app, owner, acc_b, acc_c } = await loadFixture(deploySocialActivation);
            // Authorise acc_b
            await app.connect(owner)._authorise_user(acc_b.address);
            // Make new notification with acc_b
            tx = await app.connect(acc_b)._new_notification(notification_reg.in_regions, notification_reg.in_type, notification_reg.tx_params);
            // Get Timeout value entered + Timeout variable set in smart contract
            timeout = await time.latest() + parseInt(await app.TIMEOUT());
            // Make sure all regions have been given a timestamp
            for (let i = 0; i < notification_reg.in_regions.length; i++) { 
                expect(await app.user_to_timestamp(acc_b.address, notification_reg.in_regions[i], notification_reg.in_type)).to.equal(timeout);
            }
        });
        it("Should update main notification list", async function () {
            // Deploy Contract
            const { app, owner, acc_b, acc_c } = await loadFixture(deploySocialActivation);
            // Authorise acc_b
            await app.connect(owner)._authorise_user(acc_b.address);
            // Make new notification with acc_b
            tx = await app.connect(acc_b)._new_notification(notification_reg.in_regions, notification_reg.in_type, notification_reg.tx_params);
            // Get Timeout value entered + Timeout variable set in smart contract
            timeout = await time.latest() + parseInt(await app.TIMEOUT());
            // Make sure all regions have been given a timestamp
            for (let i = 0; i < notification_reg.in_regions.length; i++) { 
                // Zero in following line is position in list inside mapping
                array_temp = await app.region_to_type_count(notification_reg.in_regions[i], notification_reg.in_type, 0);
                expect(array_temp.creator).to.equal(acc_b.address);
                expect(array_temp.times_out).to.equal(timeout);
            }
        });
        it("Should not allow second notification within time frame", async function () {
            // Deploy Contract
            const { app, owner, acc_b, acc_c } = await loadFixture(deploySocialActivation);
            // Authorise acc_b
            await app.connect(owner)._authorise_user(acc_b.address);
            // Make new notification with acc_b
            tx = await app.connect(acc_b)._new_notification(notification_reg.in_regions, notification_reg.in_type, notification_reg.tx_params);
            // Get Timeout value entered + Timeout variable set in smart contract
            timeout = await time.latest() + parseInt(await app.TIMEOUT());
            // This should fail as notification is still active
            await expect(app.connect(acc_b)._new_notification(notification_reg.in_regions, notification_reg.in_type, notification_reg.tx_params)).to.be.revertedWith("Address already has active notification at this region/type");
            // Time travel to after notification becomes inactive (5 is arbitrary)
            time.increaseTo(timeout+5);
            // This should pass as notification is inactive
            await expect(app.connect(acc_b)._new_notification(notification_reg.in_regions, notification_reg.in_type, notification_reg.tx_params)).to.not.be.reverted;
        });
        it("Should allow many notifications from unique users in same region", async function () {
            // Deploy Contract
            const { app, owner, acc_b, acc_c } = await loadFixture(deploySocialActivation);
            // Authorise acc_b and acc_c
            await app.connect(owner)._authorise_user(acc_b.address);
            await app.connect(owner)._authorise_user(acc_c.address);
            // Make new notification with all accounts
            tx_a = app.connect(owner)._new_notification(notification_reg.in_regions, notification_reg.in_type, notification_reg.tx_params);
            tx_b = app.connect(acc_b)._new_notification(notification_reg.in_regions, notification_reg.in_type, notification_reg.tx_params);
            tx_c = app.connect(acc_c)._new_notification(notification_reg.in_regions, notification_reg.in_type, notification_reg.tx_params);
            // Execute all tx
            await expect(tx_a).to.not.be.reverted;
            await expect(tx_b).to.not.be.reverted;
            await expect(tx_c).to.not.be.reverted;
        });
    });


    // ###########################################################################
    describe("View function Check Active Notifications", function () {
        it("Should return true if no notification exists (New notification is acceptable)", async function () {
            // Deploy Contract
            const { app, owner, acc_b, acc_c } = await loadFixture(deploySocialActivation);
            // Authorise acc_b
            await app.connect(owner)._authorise_user(acc_b.address);
            // Check if notification exists (Should return true)
            expect(await app.connect(acc_b)._check_active_notification(notification_reg.in_regions[0], notification_reg.in_type, notification_reg.tx_params)).to.equal(true);
        });
        it("Should return true if notification exists but is outdated (New notification is acceptable)", async function () {
            // Deploy Contract
            const { app, owner, acc_b, acc_c } = await loadFixture(deploySocialActivation);
            // Authorise acc_b
            await app.connect(owner)._authorise_user(acc_b.address);
            // Add notification
            tx = await app.connect(acc_b)._new_notification(notification_reg.in_regions, notification_reg.in_type, notification_reg.tx_params);
            // Get timestamp of when notification timeout occurs
            timeout = await time.latest() + parseInt(await app.TIMEOUT());
            // Time travel to after notification becomes inactive (5 is arbitrary)
            time.increaseTo(timeout+5);
            // Check if notification exists and is outdated (Should return true)
            expect(await app.connect(acc_b)._check_active_notification(notification_reg.in_regions[0], notification_reg.in_type, notification_reg.tx_params)).to.equal(true);
        });
        it("Should return false if notification exists and is current (New notification is not acceptable)", async function () {
            // Deploy Contract
            const { app, owner, acc_b, acc_c } = await loadFixture(deploySocialActivation);
            // Authorise acc_b
            await app.connect(owner)._authorise_user(acc_b.address);
            // Add notification
            tx = await app.connect(acc_b)._new_notification(notification_reg.in_regions, notification_reg.in_type, notification_reg.tx_params);
            // Get timestamp of when notification timeout occurs
            timeout = await time.latest() + parseInt(await app.TIMEOUT());
            // Time travel to after notification becomes inactive (5 is arbitrary)
            time.increaseTo(timeout-1);
            // Check if notification exists and is outdated (Should return true)
            expect(await app.connect(acc_b)._check_active_notification(notification_reg.in_regions[0], notification_reg.in_type, notification_reg.tx_params)).to.equal(false);
        });
    });


    // ###########################################################################
    describe ("Consensus Mechanism", function () {
        it("Should only find consensus when notification threshold met", async function () {
            // Deploy Contract
            const { app, owner, acc_b, acc_c } = await loadFixture(deploySocialActivation);
            // Authorise acc_b and acc_c
            await app.connect(owner)._authorise_user(acc_b.address);
            await app.connect(owner)._authorise_user(acc_c.address);
            // Get threshold
            threshold = parseInt(await app.THRESHOLD());
            // Make sure threshold is more than zero
            expect(threshold).to.be.above(0, "Threshold is 0 or less, this is invalid");
            // If no notifications fail
            await expect(app._confirm_consensus(notification_reg.in_regions[0], notification_reg.in_type)).to.be.revertedWith("Consensus has not been reached");
            if (threshold == 1) {
                // Consensus passes with 1 notification
                await app.connect(owner)._new_notification(notification_reg.in_regions, notification_reg.in_type, notification_reg.tx_params);
                await expect(app._confirm_consensus(notification_reg.in_regions[0], notification_reg.in_type)).to.not.be.reverted;
            } else if (threshold == 2) {
                // Consensus fails with 1 notification but passes with 2 notifications
                await app.connect(owner)._new_notification(notification_reg.in_regions, notification_reg.in_type, notification_reg.tx_params);
                await expect(app._confirm_consensus(notification_reg.in_regions[0], notification_reg.in_type)).to.be.revertedWith("Consensus has not been reached");
                await app.connect(acc_b)._new_notification(notification_reg.in_regions, notification_reg.in_type, notification_reg.tx_params);
                await expect(app._confirm_consensus(notification_reg.in_regions[0], notification_reg.in_type)).to.not.be.reverted;
            } else if (threshold == 3) {
                // Consensus fails with 1 and 2 notifications but passes with 3 notifications
                await app.connect(owner)._new_notification(notification_reg.in_regions, notification_reg.in_type, notification_reg.tx_params);
                await expect(app._confirm_consensus(notification_reg.in_regions[0], notification_reg.in_type)).to.be.revertedWith("Consensus has not been reached");
                await app.connect(acc_b)._new_notification(notification_reg.in_regions, notification_reg.in_type, notification_reg.tx_params);
                await expect(app._confirm_consensus(notification_reg.in_regions[0], notification_reg.in_type)).to.be.revertedWith("Consensus has not been reached");
                await app.connect(acc_c)._new_notification(notification_reg.in_regions, notification_reg.in_type, notification_reg.tx_params);
                await expect(app._confirm_consensus(notification_reg.in_regions[0], notification_reg.in_type)).to.not.be.reverted;
            } else {
                // If threshold is set to more than 3 test is not run
                console.log("This test only gets completed on threshold 3 or less");
            }
        });
        it("Should allow anyone to find consensus even if not authorised", async function () {
            // Deploy Contract
            const { app, owner, acc_b, acc_c, acc_d } = await loadFixture(deploySocialActivation);
            // Authorise acc_b and acc_c
            await app.connect(owner)._authorise_user(acc_b.address);
            await app.connect(owner)._authorise_user(acc_c.address);
            // Get threshold
            threshold = parseInt(await app.THRESHOLD());
            if (threshold <= 3) {
                await app.connect(owner)._new_notification(notification_reg.in_regions, notification_reg.in_type, notification_reg.tx_params);
                await app.connect(acc_b)._new_notification(notification_reg.in_regions, notification_reg.in_type, notification_reg.tx_params);
                await expect(app.connect(acc_d)._confirm_consensus(notification_reg.in_regions[0], notification_reg.in_type)).to.be.revertedWith("Consensus has not been reached");
                await app.connect(acc_c)._new_notification(notification_reg.in_regions, notification_reg.in_type, notification_reg.tx_params);
                await expect(app.connect(acc_d)._confirm_consensus(notification_reg.in_regions[0], notification_reg.in_type)).to.not.be.reverted;
            } else {
                // If threshold is set to more than 3 test is not run
                console.log("This test only gets completed on threshold 3 or less");
            }
        });
        it("Should clear notifications when consensus found", async function () {
            // Deploy Contract
            const { app, owner, acc_b, acc_c } = await loadFixture(deploySocialActivation);
            // Authorise acc_b and acc_c
            await app.connect(owner)._authorise_user(acc_b.address);
            await app.connect(owner)._authorise_user(acc_c.address);
            // Get threshold
            threshold = parseInt(await app.THRESHOLD());
            if (threshold <= 3) {
                await app.connect(owner)._new_notification(notification_reg.in_regions, notification_reg.in_type, notification_reg.tx_params);
                await app.connect(acc_b)._new_notification(notification_reg.in_regions, notification_reg.in_type, notification_reg.tx_params);
                await expect(app._confirm_consensus(notification_reg.in_regions[0], notification_reg.in_type)).to.be.revertedWith("Consensus has not been reached");
                await app.connect(acc_c)._new_notification(notification_reg.in_regions, notification_reg.in_type, notification_reg.tx_params);
                // Pass as list exists
                expect(app.region_to_type_count(notification_reg.in_regions[0], notification_reg.in_type, 0)).to.not.be.reverted;
                // Find consensus which should clear list
                await expect(app._confirm_consensus(notification_reg.in_regions[0], notification_reg.in_type)).to.not.be.reverted;
                // Fail as list no longer exists
                expect(app.region_to_type_count(notification_reg.in_regions[0], notification_reg.in_type, 0)).to.be.reverted;
            } else {
                // If threshold is set to more than 3 test is not run
                console.log("This test only gets completed on threshold 3 or less");
            }
        });
        it("Should not find consensus twice in a row without new notifications", async function () {
            // Deploy Contract
            const { app, owner, acc_b, acc_c } = await loadFixture(deploySocialActivation);
            // Authorise acc_b and acc_c
            await app.connect(owner)._authorise_user(acc_b.address);
            await app.connect(owner)._authorise_user(acc_c.address);
            // Get threshold
            threshold = parseInt(await app.THRESHOLD());
            if (threshold <= 3) {
                await app.connect(owner)._new_notification(notification_reg.in_regions, notification_reg.in_type, notification_reg.tx_params);
                await app.connect(acc_b)._new_notification(notification_reg.in_regions, notification_reg.in_type, notification_reg.tx_params);
                await expect(app._confirm_consensus(notification_reg.in_regions[0], notification_reg.in_type)).to.be.revertedWith("Consensus has not been reached");
                await app.connect(acc_c)._new_notification(notification_reg.in_regions, notification_reg.in_type, notification_reg.tx_params);
                // Find consensus which should clear list
                await expect(app._confirm_consensus(notification_reg.in_regions[0], notification_reg.in_type)).to.not.be.reverted;
                // Fail as consensus not found twice in a row
                await expect(app._confirm_consensus(notification_reg.in_regions[0], notification_reg.in_type)).to.be.revertedWith("Consensus has not been reached");
            } else {
                // If threshold is set to more than 3 test is not run
                console.log("This test only gets completed on threshold 3 or less");
            }
        });
    });

    
    // ###########################################################################
    describe("View function Count Rep in Region", function () {
        it("Should be callable by all", async function () {
            // Deploy Contract
            const { app, owner, acc_b, acc_c } = await loadFixture(deploySocialActivation);
            await app.connect(owner)._new_notification(notification_reg.in_regions, notification_reg.in_type, notification_reg.tx_params);
            // Count a notification if it is in date
            expect(await app.connect(acc_b)._count_region(notification_reg.in_regions[0], notification_reg.in_type)).to.be.above(0);
        });
        it("Should count 0 if region or type is not in boundaries", async function () {
            // Deploy Contract
            const { app, owner, acc_b, acc_c } = await loadFixture(deploySocialActivation);
            max_region = parseInt(await app.MAX_REGION());
            // Make a random notification
            await app.connect(owner)._new_notification(notification_reg.in_regions, notification_reg.in_type, notification_reg.tx_params);
            // Pass if output from invalid region is zero
            expect(await app._count_region(max_region+10, notification_reg.in_type)).to.equal(0);
        });
        it("Should count 0 if no notifications exist for region", async function () {
            // Deploy Contract
            const { app, owner, acc_b, acc_c } = await loadFixture(deploySocialActivation);
            max_region = parseInt(await app.MAX_REGION());
            // Pass if output from a valid region is zero when no notifications have been created
            expect(await app._count_region(max_region-5, notification_reg.in_type)).to.equal(0);
        });
        it("Should not count out of date notifications", async function () {
            // Deploy Contract
            const { app, owner, acc_b, acc_c } = await loadFixture(deploySocialActivation);
            await app.connect(owner)._new_notification(notification_reg.in_regions, notification_reg.in_type, notification_reg.tx_params);
            // Count a notification if it is in date
            expect(await app._count_region(notification_reg.in_regions[0], notification_reg.in_type)).to.be.above(0);
            // Time travel to after notification becomes out of date (5 is arbitrary)
            timeout = await time.latest() + parseInt(await app.TIMEOUT());
            time.increaseTo(await timeout + 50);
            new_time = await time.latest();
            // Do not count a notification if it is out of date
            expect(await app._count_region(notification_reg.in_regions[0], notification_reg.in_type)).to.equal(0);
        });
        it("Should count correctly for real notifications", async function () {
            // Deploy Contract
            const { app, owner, acc_b, acc_c } = await loadFixture(deploySocialActivation);
            // Authorise acc_b and acc_c
            await app.connect(owner)._authorise_user(acc_b.address);
            await app.connect(owner)._authorise_user(acc_c.address);
            // Get rep of address'
            rep_owner = parseInt(await app._get_rep(owner.address));
            rep_acc_b = parseInt(await app._get_rep(acc_b.address));
            rep_acc_c = parseInt(await app._get_rep(acc_c.address));
            // Make new notifications and count region
            expect(await app._count_region(notification_reg.in_regions[0], notification_reg.in_type)).to.equal(0);
            await app.connect(owner)._new_notification(notification_reg.in_regions, notification_reg.in_type, notification_reg.tx_params);
            expect(await app._count_region(notification_reg.in_regions[0], notification_reg.in_type)).to.equal(rep_owner);
            await app.connect(acc_b)._new_notification(notification_reg.in_regions, notification_reg.in_type, notification_reg.tx_params);
            expect(await app._count_region(notification_reg.in_regions[0], notification_reg.in_type)).to.equal(rep_owner+rep_acc_b);
            await app.connect(acc_c)._new_notification(notification_reg.in_regions, notification_reg.in_type, notification_reg.tx_params);
            expect(await app._count_region(notification_reg.in_regions[0], notification_reg.in_type)).to.equal(rep_owner+rep_acc_b+rep_acc_c);
            threshold = parseInt(await app.THRESHOLD());
            if (threshold <= 3) {
                // Find consensus to reset and to improve rep to count with different rep
                await expect(app._confirm_consensus(notification_reg.in_regions[0], notification_reg.in_type)).to.not.be.reverted;
                rep_owner = parseInt(await app._get_rep(owner.address));
                rep_acc_b = parseInt(await app._get_rep(acc_b.address));
                rep_acc_c = parseInt(await app._get_rep(acc_c.address));
                // Count region
                expect(await app._count_region(notification_reg.in_regions[1], notification_reg.in_type)).to.equal(rep_owner+rep_acc_b+rep_acc_c);
                // Find consensus to reset and to improve rep to count with different rep
                await expect(app._confirm_consensus(notification_reg.in_regions[1], notification_reg.in_type)).to.not.be.reverted;
                rep_owner = parseInt(await app._get_rep(owner.address));
                rep_acc_b = parseInt(await app._get_rep(acc_b.address));
                rep_acc_c = parseInt(await app._get_rep(acc_c.address));
                // Count region
                expect(await app._count_region(notification_reg.in_regions[2], notification_reg.in_type)).to.equal(rep_owner+rep_acc_b+rep_acc_c);
            } else {
                console.log("Test only partially completed. Fully completed if threshold is 3 or less");
            }
        });
    });


    // ###########################################################################
    describe("View function Calculate Reputation", function () {
        it("Should return value > 0 for active address", async function () {
            // Deploy Contract
            const { app, owner, acc_b, acc_c } = await loadFixture(deploySocialActivation);
            // Authorise acc_b and acc_c
            await app.connect(owner)._authorise_user(acc_b.address);
            // Check result is above 0
            expect(await app._get_rep(acc_b.address)).to.be.above(0);
        });
        it("Should return 0 for non-active address", async function () {
            // Deploy Contract
            const { app, owner, acc_b, acc_c } = await loadFixture(deploySocialActivation);
            // Check result is equal to zero
            expect(await app._get_rep(acc_b.address)).to.equal(0);
        });
        it("Should be callable by non-authorised address'", async function () {
            // Deploy Contract
            const { app, owner, acc_b, acc_c } = await loadFixture(deploySocialActivation);
            // Check result is equal to zero
            expect(await app.connect(acc_b)._get_rep(owner.address)).to.be.above(0);
        });
        it("Reputation Calculated correctly", async function () {
            expect(1).to.equal(0, "Reputation Engine not complete")
        });
    });

    
});