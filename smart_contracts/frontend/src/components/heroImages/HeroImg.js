// ---------- Copyright (C) 2024 University of Strathclyde and Author ---------
// ------------------------- Author: Robert Cowlishaw -------------------------
// -------------- e-mail: robert.cowlishaw.2017@uni.strath.ac.uk --------------

import "./HeroImgStyles.css";
import { React } from "react";

import HomeImg from "../../assets/home-img.jpg";
//import { Link } from "react-router-dom";

export const HeroImg = () => {
  return (
    <div className="hero">
      <img className="intro-img" src={HomeImg} alt='Hero' />

      <div className="content">
       <h1>DisasterWeb</h1>
        <p>Consensus across Natural Disasters</p>  
        {/* <div>
          <Link to="/project" className="btn btn-light">
            Social Activation
          </Link>
          <Link to="/contact" className="btn btn-light">
            Automatic Tasking
          </Link>
          <Link to="/contact" className="btn btn-light">
            Data Consensus
          </Link>
        </div> */}
      </div>
    </div>
  );
};

