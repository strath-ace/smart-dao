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

