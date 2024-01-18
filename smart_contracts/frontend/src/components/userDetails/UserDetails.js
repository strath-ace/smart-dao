

export const UserDetails = ({params}) => {
    return (
        <>
            <div className="account-heading">
                <h3>User: {params.user_address}</h3>
            </div>
        </>
        );
}