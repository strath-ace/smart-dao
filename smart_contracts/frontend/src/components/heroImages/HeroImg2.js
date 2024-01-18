// ---------- Copyright (C) 2024 University of Strathclyde and Author ---------
// ------------------------- Author: Robert Cowlishaw -------------------------
// -------------- e-mail: robert.cowlishaw.2017@uni.strath.ac.uk --------------

import "./HeroImg2Styles.css";
//import React, { Component } from "react";

import Image_of_the_back from "../../assets/social-activation-img.jpg";

// export class HeroImg2 extends Component {
//   render() {
//       return (
//         <div className="hero">
//           <div className="mask">
//             <img className="hero-img" src={Image_of_the_back} alt='Background Img' />
//           </div>

//           <div className="heading">
//             <h1>{this.props.heading}</h1>
//             <p> {this.props.text} </p>
//           </div>
//         </div>
//          );
//   }
// };

export const HeroImg2 = ({heading, text}) => {
  return (
    <div>
      <div className="hero-img">
        <img src={Image_of_the_back} alt='Background' />
      </div>
      <div className="hero-heading">
        <h1>{heading}</h1>
        <p> {text} </p>
      </div>
    </div>
    // <div className="hero">
    // </div>
  );
}

