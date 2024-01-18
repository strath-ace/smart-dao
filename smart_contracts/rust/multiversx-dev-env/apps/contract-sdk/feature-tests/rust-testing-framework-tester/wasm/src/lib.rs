// Code generated by the multiversx-sc multi-contract system. DO NOT EDIT.

////////////////////////////////////////////////////
////////////////// AUTO-GENERATED //////////////////
////////////////////////////////////////////////////

// Init:                                 1
// Endpoints:                           26
// Async Callback:                       1
// Total number of exported functions:  28

#![no_std]
#![feature(alloc_error_handler, lang_items)]

multiversx_sc_wasm_adapter::allocator!();
multiversx_sc_wasm_adapter::panic_handler!();

multiversx_sc_wasm_adapter::endpoints! {
    rust_testing_framework_tester
    (
        sum
        sum_sc_result
        get_caller_legacy
        get_egld_balance
        get_esdt_balance
        receive_egld
        recieve_egld_half
        receive_esdt
        reject_payment
        receive_esdt_half
        receive_multi_esdt
        send_nft
        mint_esdt
        burn_esdt
        create_nft
        get_block_epoch
        get_block_nonce
        get_block_timestamp
        get_random_buffer_once
        get_random_buffer_twice
        call_other_contract_execute_on_dest
        call_other_contract_add_async_call
        getTotalValue
        execute_on_dest_add_value
        addValue
        panic
        callBack
    )
}