import React from "react";

import { Navbar } from "../components/navbar/Navbar";
import { HeroImg2 } from "../components/heroImages/HeroImg2";

import { UserDetails } from "../components/userDetails/UserDetails"
import { Authoriser } from "../components/authoriser/Authoriser"


import "../components/userDetails/UserDetailsStyle.css"

export const WalletInfo = ({params}) => {
  return (
    <div>
      <Navbar params={params}/>
      <HeroImg2 heading={"Account Info"} text={"Your account details"} />
      <UserDetails params={params} />
      <Authoriser params={params} />
      {/* <PriceCardList />
      <Work /> 
      <Footer />*/}
    </div>
  );
};

