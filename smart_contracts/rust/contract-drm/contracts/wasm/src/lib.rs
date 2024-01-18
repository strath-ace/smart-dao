// Code generated by the multiversx-sc multi-contract system. DO NOT EDIT.

////////////////////////////////////////////////////
////////////////// AUTO-GENERATED //////////////////
////////////////////////////////////////////////////

// Init:                                 1
// Endpoints:                            8
// Async Callback (empty):               1
// Total number of exported functions:  10

#![no_std]
#![feature(alloc_error_handler, lang_items)]

multiversx_sc_wasm_adapter::allocator!();
multiversx_sc_wasm_adapter::panic_handler!();

multiversx_sc_wasm_adapter::endpoints! {
    contracts
    (
        new_warning
        new_disaster
        disaster_template_address
        getWarningTimestamp
        getWarningData
        getWarningCreator
        isActiveWarning
        getFirstActiveWarning
    )
}

multiversx_sc_wasm_adapter::empty_callback! {}
