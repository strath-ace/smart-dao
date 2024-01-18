// ---------- Copyright (C) 2024 University of Strathclyde and Author ---------
// ------------------------- Author: Robert Cowlishaw -------------------------
// -------------- e-mail: robert.cowlishaw.2017@uni.strath.ac.uk --------------

import React from "react";
import { Navbar } from "../components/navbar/Navbar";
//import { Footer } from "../components/footer/Footer";
import { HeroImg2 } from "../components/heroImages/HeroImg2";
//import { PriceCardList } from "../components/priceCards/PriceCardList";
//import { Work } from "../components/work/Work";
import { SocialActivationApp } from "../components/socialActivation/SocialActivationApp";

//import "../components/socialActivation/SocialActivationStyle.css"

export const SocialActivation = ({params}) => {
  return (
    <div>
      <Navbar params={params}/>
      <HeroImg2 heading={"SOCIAL ACTIVATION"} text={"Determine if, where and when a disaster has occured"} />
      <SocialActivationApp params={params}/>
      {/* <PriceCardList />
      <Work /> 
      <Footer />*/}
    </div>
  );
};

