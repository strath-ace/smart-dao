// #![no_std]

// multiversx_sc::imports!();
// multiversx_sc::derive_imports!();

// pub const TIMESTAMP_WINDOW: u64 = 1000000000;

// // Warning Type Structure
// #[derive(TypeAbi, TopEncode, TopDecode, PartialEq, Debug)]
// pub struct Warning<M: ManagedTypeApi> {
//     pub disaster_type: u8,
//     pub timestamp: u64,
//     pub lat: u32,
//     pub lon: u32,
//     pub sender: ManagedAddress<M>,
// }

// // Initial Deployed Main Class
// #[multiversx_sc::contract]
// pub trait Main {


//     // ---------- STORAGE MAPPERS ----------

//     // Mapping - "Disaster Template Address" -> Contract Address
//     #[view]
//     #[storage_mapper("disasterTempalteAddress")]
//     fn disaster_template_address(&self) -> SingleValueMapper<BigUint>;

//     // Mapping - "Warning Number" -> Int
//     #[view(getWarningNumber)]
//     #[storage_mapper("warningNumber")]
//     // May have to fix u64 for overflow at some point
//     fn warning_number(&self) -> SingleValueMapper<u64>;

//     // Mapping - Address -> Confidence in Address

//     // Mapping - Warning Number -> Warning
//     #[view(getWarning)]
//     #[storage_mapper("warning")]
//     // May have to fix u64 for overflow at some point
//     fn get_warning(&self, warning_number: u64) -> SingleValueMapper<Warning<Self::Api>>;


//     // ---------- INIT METHOD ----------

//     // Initiate Method for Class
//     #[init]
//     fn init(&self, input_address: BigUint) {
//         self.warning_number().set(0);
//         self.disaster_template_address().set(input_address);
//     }


//     // ---------- FUNCTIONAL IF STATEMENTS ----------

//     // Checks if warning number is active warning
//     #[view(isActiveWarning)]
//     fn is_active_warning(&self, warning_number: u64) -> bool {
//         return self.get_warning(warning_number).get().timestamp + TIMESTAMP_WINDOW >= self.blockchain().get_block_timestamp();
//     }


//     // ---------- CLASS METHODS ----------

//     // Gets the warning number of the oldest active warning
//     #[view(getFirstActiveWarning)]
//     fn get_first_active_warning(&self) -> u64 {
//         let mut c:u64 = self.warning_number().get();
//         while c > 0 && self.is_active_warning(c) {
//             c -= 1;
//         }
//         return c+1;
//     }

//     // Validate sender is allowed to make changes
//     fn validate_source(&self) {
//         require!(
//             true,   // Add conditions
//             "Sender does not hold required credentials"
//         );
//     }

//     // Creates new warning and saves to mapping
//     #[endpoint]
//     fn create_warning(&self, disaster_type: u8, lat: u32, lon: u32) {
//         self.validate_source();
//         // Disaster type matches 1.EQ, 2.TC, 3.FL, 4.VO, 5.DR, 6.WF
//         require!(disaster_type <= 5, "Invalid disaster type");
//         // Latitude and Loniguted in correct ranges
//         require!(
//             (lat <= 180_000) && (lon < 360_000),    // No need for negative comparison as u32 must be positive
//             "Latitude and/or Longitude is out of range (0.000 <= lat <= 180.000) (0.000 <= lon < 360.000)"
//         );
//         // Create new Warning Structure
//         let new_warning:Warning<<Self as ContractBase>::Api> = Warning {
//             disaster_type: disaster_type,
//             timestamp: self.blockchain().get_block_timestamp(),
//             lat: lat,
//             lon: lon,
//             sender: self.blockchain().get_caller(),
//         };
//         // Increase warning_number by 1 and save Warning with new ID
//         self.warning_number().update(|number: &mut u64| *number += 1);
//         self.get_warning(self.warning_number().get()).set(new_warning);
        
//     }

//     // Check if warnings timed out (Dont need)

//     // Check if part of current disaster

//     // Check if new disaster
//     #[endpoint]
//     fn check_for_disaster(&self) {

//     }

// }




