// ---------- Copyright (C) 2024 University of Strathclyde and Author ---------
// ------------------------- Author: Robert Cowlishaw -------------------------
// -------------- e-mail: robert.cowlishaw.2017@uni.strath.ac.uk --------------

import React from "react";
import { Navbar }   from "../components/navbar/Navbar";
//import { Footer }   from "../components/footer/Footer";
import { HeroImg2 }   from "../components/heroImages/HeroImg2";
//import { AboutContent } from "../components/about/AboutContent";

export const InformationConsensus = ({params}) => {
  return (
    <div>
      <Navbar params={params}/>
      <HeroImg2 heading="INFORMATION CONSENSUS" text="Determine the credibility of data" />
      {/* <AboutContent/>
      <Footer /> */}
    </div>
  );
};
