#![no_std]

multiversx_sc::imports!();
multiversx_sc::derive_imports!();


pub const TIMESTAMP_WINDOW: u64 = 1000000000;

// Warning Type Structure
#[derive(TypeAbi, TopEncode, TopDecode, NestedEncode, NestedDecode, PartialEq, Debug)]
pub struct Warning {
    id: u64,
    pub disaster_type: u8,
    pub lat: u32,
    pub lon: u32,
}

// Initial Deployed Main Class
#[multiversx_sc::module]
pub trait WarningModule {



    // ---------- STORAGE MAPPERS ----------

    // Mapping - "Disaster Template Address" -> Contract Address
    #[view]
    #[storage_mapper("disasterTemplateAddress")]
    fn disaster_template_address(&self) -> SingleValueMapper<ManagedAddress>;

    // Mapping - "Warning Number" -> Int
    // #[view(getWarningNumber)]
    // #[storage_mapper("warningNumber")]
    // // May have to fix u64 for overflow at some point
    // fn warning_number(&self) -> SingleValueMapper<u64>;

    // Mapping - Address -> Confidence in Address

    // Warning Ids to timestamp
    #[view(getWarningTimestamp)]
    #[storage_mapper("warningTimestamp")]
    fn get_warning_timestamp(&self) -> VecMapper<u64>;

    // Mapping - Warning Number -> Warning
    #[view(getWarningData)]
    #[storage_mapper("warningData")]
    // May have to fix u64 for overflow at some point
    fn get_warning_data(&self, warning_number: u64) -> SingleValueMapper<Warning>;

    // Mapping - Warning Number -> Creator/Sender
    #[view(getWarningCreator)]
    #[storage_mapper("warningCreator")]
    fn get_warning_creator(&self, warning_number: u64) -> SingleValueMapper<ManagedAddress>;


    // ---------- FUNCTIONAL IF STATEMENTS ----------

    // Checks if warning number is active warning
    #[view(isActiveWarning)]
    fn is_active_warning(&self, warning_number: u64) -> bool {
        return self.get_warning_timestamp().get(warning_number as usize) + TIMESTAMP_WINDOW >= self.blockchain().get_block_timestamp();
    }


    // ---------- CLASS METHODS ----------

    // Gets the warning number of the oldest active warning
    #[view(getFirstActiveWarning)]
    fn get_oldest_active_warning(&self) -> u64 {
        let mut c:u64 = self.get_warning_timestamp().len() as u64;
        while c > 0 && self.is_active_warning(c) {
            c -= 1;
        }
        return c;
    }

    // Validate sender is allowed to make changes
    fn validate_source(&self) {
        require!(
            true,   // Add conditions
            "Sender does not hold required credentials"
        );
    }

    fn check_if_warning(&self, disaster_type: u8, lat: u32, lon: u32) {
        self.validate_source();
        // Disaster type matches 1.EQ, 2.TC, 3.FL, 4.VO, 5.DR, 6.WF
        require!(disaster_type <= 5, "Invalid disaster type");
        // Latitude and Loniguted in correct ranges
        require!(
            (lat <= 180_000) && (lon < 360_000),    // No need for negative comparison as u32 must be positive
            "Latitude and/or Longitude is out of range (0.000 <= lat <= 180.000) (0.000 <= lon < 360.000)"
        );
    }

    fn build_warning(&self, disaster_type: u8, lat: u32, lon: u32) {
        // Save timestamp
        self.get_warning_timestamp().push(&self.blockchain().get_block_timestamp());
        // Save creator
        self.get_warning_creator(self.get_warning_timestamp().len() as u64).set(self.blockchain().get_caller());
        // Create new Warning Structure
        let new_warning: Warning = Warning {
            id: self.get_warning_timestamp().len() as u64,
            disaster_type: disaster_type,
            lat: lat,
            lon: lon
        };
        // Save new warning
        self.get_warning_data(self.get_warning_timestamp().len() as u64).set(new_warning);
    }

    // Check if warnings timed out (Dont need)

    // Check if part of current disaster

    // Check if new disaster
    fn check_for_disaster(&self) {
        let oldest_warning:u64 = self.get_oldest_active_warning();
        let newest_warning:u64 = self.get_warning_timestamp().len() as u64;

        for i in oldest_warning..newest_warning {
            
        }
    }


}




