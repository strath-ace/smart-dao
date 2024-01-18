// ---------- Copyright (C) 2024 University of Strathclyde and Author ---------
// ------------------------- Author: Robert Cowlishaw -------------------------
// -------------- e-mail: robert.cowlishaw.2017@uni.strath.ac.uk --------------

import React from "react";
import { Navbar } from "../components/navbar/Navbar";
import { HeroImg } from "../components/heroImages/HeroImg";
//import { Footer } from "../components/footer/Footer";
//import { Work } from "../components/work/Work";
export const Home = ({params}) => {
  return (
    <div>
      <Navbar params={params}/>
      <HeroImg />
      {/* <Work/>
      <Footer /> */}
    </div>
  );
};
 
