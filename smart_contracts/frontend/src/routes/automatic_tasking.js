// ---------- Copyright (C) 2024 University of Strathclyde and Author ---------
// ------------------------- Author: Robert Cowlishaw -------------------------
// -------------- e-mail: robert.cowlishaw.2017@uni.strath.ac.uk --------------

import React from "react";
import { Navbar } from "../components/navbar/Navbar";
//import { Footer } from "../components/footer/Footer";
import { HeroImg2 } from "../components/heroImages/HeroImg2";
//import { ContactForm } from "../components/contact/ContactForm";


export const AutomaticTasking = ({params}) => {
  return (
    <div>
      <Navbar params={params}/>
      <HeroImg2 heading="AUTOMATIC TASKING" text="Collecting data while minimising human interaction" />
      {/* <ContactForm />
      <Footer /> */}
    </div>
  );
};

