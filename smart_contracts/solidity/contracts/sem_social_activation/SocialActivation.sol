// ---------- Copyright (C) 2024 University of Strathclyde and Author ---------
// ------------------------- Author: Robert Cowlishaw -------------------------
// -------------- e-mail: robert.cowlishaw.2017@uni.strath.ac.uk --------------

pragma solidity ^0.8.9;

// console.log command
import "hardhat/console.sol";


/// @title Social Activation of a Disaster from Disaster Notifications
/// @author Robert Cowlishaw
/// @notice Allows authorised users to add notifications and when consensus is reached create a list of disasters
/// @dev Remove console.sol before final deploy
/// @dev Could add incentivisation through staking
/// @dev NEED TO ADD EMIT EVENTS
/// @dev No test for my_notification_list
/// @dev Consolidate user_to_timestamp into my_notification_list
contract SocialActivation {

    // Minimum number of votes required for consensus to be reached
    uint256 public THRESHOLD = 3;
    // Max time after creation that notification is considered active
    uint256 public TIMEOUT = 1000;
    // Max number of regions available (Currently 1 degree lat lon)
    uint256 public MAX_REGION = 360 * 180;
    // Number of types of disasters
    uint8 public NUM_DISASTER_TYPES = 5;    // One more than given as 0 also allowed
    // Counter for number of confirmed disasters
    uint256 public num_disasters;

    uint256 public MAX_TIME = 9999999999999;


    // Disaster Notifications
    struct Notification {
        address creator;
        uint times_out;
    }

    struct MyNotification {
        uint disaster_type;
        uint region;
        uint timestamp;
    }

    // Confirmed Disasters
    struct Disaster {
        uint disaster_type;
        uint region;
        uint time_of_first_notification;
        uint time_of_consensus;
    }


    // Is user authorised
    // Address to authorised
    mapping (address => bool) public get_authorised;

    // Notifications made
    // Address to number of total notifications
    mapping (address => uint) public num_notifications;

    // Notifications part of consensus
    // Address to number of correct notifications
    mapping (address => uint) public num_correct_notifications;

    // List of all Notifications
    // Region to type to Notifications list
    mapping (uint => mapping (uint => Notification[])) public region_to_type_count;

    // List of all an address' notification
    // Address to MyNotifications list
    mapping (address => MyNotification[]) public my_notification_list;

    // List of Notifications for specific user
    // User to region to type to timestamp
    mapping (address => mapping (uint => mapping (uint => uint) ) ) public user_to_timestamp;

    // List of disasters
    // Disaster ID to Disaster list
    mapping (uint => Disaster) public disasters_confirmed;

    
    /// @notice On deploy constructor
    /// @dev Maybe set owner to reputation of zero also, could also add address as input to create the first authorised user
    constructor() {
        get_authorised[msg.sender] = true;
        num_notifications[msg.sender] = 1;
        num_correct_notifications[msg.sender] = 1;
    }

    
    /// @notice Authorises input user address'
    /// @dev (PUBLIC)
    /// @param _new_address New address to authorise (address)
    function _authorise_user(address _new_address) public {
        require(get_authorised[msg.sender] == true, "Only authorised users can authorise new users");
        require(get_authorised[_new_address] == false, "New user is already authorised");
        get_authorised[_new_address] = true;
        num_notifications[_new_address] = 1;
        num_correct_notifications[_new_address] = 1;
    }


    /// @notice Creates new notification, including validating that notification is allowed to be given by user
    /// @dev (PUBLIC)
    /// @param _regions Array of regions of notification (uint[])
    /// @param _disaster_type Type of disaster of notification (uint)
    function _new_notification(uint[] memory _regions, uint _disaster_type) public {
        require(get_authorised[msg.sender] == true, "User is not authorised");
        require(_disaster_type <= NUM_DISASTER_TYPES, "Not a classified type of disaster (0-5)");
        Notification memory notification = Notification({
            creator: msg.sender,
            times_out: block.timestamp + TIMEOUT
            // Could add stake amount too
        });
        // Increment how many notifications a user has made
        num_notifications[msg.sender] += _regions.length;
        // Checks if user has active notification in region/type and if not adds new notification
        for (uint i = 0; i < _regions.length; i++) {
            require(_check_active_notification(_regions[i], _disaster_type), "Address already has active notification at this region/type");
            require(_regions[i] <= MAX_REGION, "Region is outside maximum value");
            user_to_timestamp[msg.sender][_regions[i]][_disaster_type] = block.timestamp + TIMEOUT;
            region_to_type_count[_regions[i]][_disaster_type].push(notification);
            MyNotification memory my_notification = MyNotification({
                disaster_type: _disaster_type,
                region: _regions[i],
                timestamp: block.timestamp
            });
            my_notification_list[msg.sender].push(my_notification);
        }
        
    }


    /// @notice Checks if the user already has an active notification at this region
    /// @dev (PUBLIC VIEW)
    /// @param _region Region of notification to check (uint)
    /// @param _disaster_type Type of disaster of notification to check (uint)
    /// @return active If the region/type has no active notification by the msg.sender (Bool)
    function _check_active_notification(uint _region, uint _disaster_type) public view returns (bool active) {
        active = user_to_timestamp[msg.sender][_region][_disaster_type] < block.timestamp;
        return active;
    }


    /// @notice Checks if consensus exists in given region/type, creates disaster_confirmed value, deletes notifications in given region/type
    /// @dev (PUBLIC)
    /// @param _region Region of notifications to check for (uint)
    /// @param _disaster_type Type of disaster of notification to check for (uint)
    function _confirm_consensus(uint _region, uint _disaster_type) public {
        // Counts reputation from all notifications in given region/type
        require(_region <= MAX_REGION);
        require(_disaster_type <= NUM_DISASTER_TYPES);
        uint count = _count_region(_region, _disaster_type);
        require(count >= THRESHOLD, "Consensus has not been reached");
        uint first_notification = MAX_TIME;
        // Update correct notifications count
        Notification[] memory current_region = region_to_type_count[_region][_disaster_type];
        for (uint i = 0; i < current_region.length; i++) {
            if (current_region[i].times_out > block.timestamp) {
                num_correct_notifications[current_region[i].creator]++;
                if (current_region[i].times_out < first_notification) {
                    first_notification = current_region[i].times_out;
                }
            }
        }
        // Creates confirmed disaster
        num_disasters++;
        disasters_confirmed[num_disasters] = Disaster({
            disaster_type: _disaster_type,
            region: _region,
            time_of_first_notification: first_notification - THRESHOLD,
            time_of_consensus: block.timestamp
        });
        // Remove all notifications for that region and disaster type after consensus found
        delete region_to_type_count[_region][_disaster_type];
        // Maybe incentivise by giving 10% stake to msg.sender at this point
    }


    /// @notice Counts total reputation of all active notifications in the input region/type
    /// @dev (PUBLIC VIEW)
    /// @param _region Region of notifications to check for (uint)
    /// @param _disaster_type Type of disaster of notification to check for (uint)
    /// @return count Total reputation (uint)
    function _count_region(uint _region, uint _disaster_type) public view returns (uint count) {
        count = 0;
        Notification[] memory current_region = region_to_type_count[_region][_disaster_type];
        for (uint i = 0; i < current_region.length; i++) {
            if (current_region[i].times_out > block.timestamp) {
                count += _get_rep(current_region[i].creator);
            }
        }
        return count;
    }


    /// @notice Gets reputation of input address
    /// @dev (PUBLIC VIEW) Needs modified as currently very simple 
    /// @param _address_to_update Address to get the reputation of (address)
    /// @return rep Reputation of the input address (uint)
    function _get_rep(address _address_to_update) public view returns (uint rep) {
        // Can use number of correct notifications and number of total notifications
        rep = num_correct_notifications[_address_to_update];// / num_notifications[_address_to_update];
        return rep;
    }


    
    function _get_my_notification_list(address _address_to_check) public view returns (MyNotification[] memory) {
        return my_notification_list[_address_to_check];
    }

    function _get_disaster_count() public view returns (uint) {
        return num_disasters;
    }

    function _get_disasters_list(uint _disaster_id) public view returns (Disaster memory) {
        return disasters_confirmed[_disaster_id];
    }
}