// drm_main.rs
// This works as a contract handler for both drm_warning and drm_disaster_c*.
// This is the interface point for interaction with drm contracts.


#![no_std]


multiversx_sc::imports!();
multiversx_sc::derive_imports!();



pub mod drm_warning;

// Initial Deployed Main Class
#[multiversx_sc::contract]
pub trait Main: 
    drm_warning::WarningModule {

    // ---------- INIT METHOD ----------

    // Initiate Method for Class
    #[init]
    fn init(&self, input_address: ManagedAddress) {
        //self.warning_number().set(0);
        self.disaster_template_address().set(input_address);
        //self.set_initial_len(&self, u64::MAX);
    }

    // Creates new warning and saves to mapping
    #[endpoint]
    fn new_warning(&self, disaster_type: u8, lat: u32, lon: u32) {
        self.check_if_warning(disaster_type, lat, lon);
        self.build_warning(disaster_type, lat, lon);
    }
    

    #[endpoint]
    fn new_disaster(&self) {
        self.check_for_disaster()
    }

}




