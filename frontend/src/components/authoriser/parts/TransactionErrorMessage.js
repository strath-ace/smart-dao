import React from "react";

export function TransactionErrorMessage({ message, dismiss }) {
  // var err_out;
  // try {
  //   message = message.toString()
  //   var counter = 0;
  //   var start_point = -1;
  //   for (let i = 0; i < message.length; i++) {
  //     if (start_point < 0 & (message.substring(i,i+7) === "error={")) {
  //       start_point = i+6;
  //     }
  //     if (start_point >= 0 & message[i] === "{") {
  //       counter += 1;
  //     }
  //     if (start_point >= 0 & message[i] === "}") {
  //       counter -= 1;
  //     }
  //     if (start_point >= 0 & counter === 0 & message[i] === "}") {
  //       var end_point = i+1;
  //       break;
  //     }
  //   }

  //   var err_json = message.substring(start_point,end_point);
  //   err_json = JSON.parse(err_json);
  //   err_out = err_json["data"]["message"];
  //   if (err_out === undefined) {
  //     throw "Error is not accounted for, therefore display all error data";
  //   }
  // } 
  // catch(err) {
  //   console.log(err);
  //   err_out = message.substring(0, 200);
  // }
  var err_out;
  try{
    err_out = message.error.message;
  }
  catch (err) {
    err_out = (JSON.stringify(message));
  }
  return (
    <div className="alert alert-danger" role="alert">
      Error sending transaction: {err_out}
      <button
        type="button"
        className="close"
        data-dismiss="alert"
        aria-label="Close"
        onClick={dismiss}
      >
        <span aria-hidden="true">&times;</span>
      </button>
    </div>
  );
}
