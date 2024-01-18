// ---------- Copyright (C) 2024 University of Strathclyde and Author ---------
// ------------------------- Author: Robert Cowlishaw -------------------------
// -------------- e-mail: robert.cowlishaw.2017@uni.strath.ac.uk --------------

export const UserDetails = ({params}) => {
    return (
        <>
            <div className="account-heading">
                <h3>User: {params.user_address}</h3>
            </div>
        </>
        );
}