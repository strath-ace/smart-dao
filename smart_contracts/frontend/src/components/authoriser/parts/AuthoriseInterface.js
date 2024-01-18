import React from "react";

export function AuthoriseInterface({func_authorise}) {

  function authorise() {
    var _address = document.getElementById("address_box");
    if (_address.value === "") {
      console.log("Empty Type or Regions of Disaster");
    } else {
      func_authorise(_address.value);
    }
  }

  return (
    <div>
      <h4>Authorise New User</h4>
        
        <div className="form-group">
          <label>Address to authorise (If you are already authorised)</label>
          <input id="address_box" className="form-control" step="1" name="_type" placeholder="Address 0x..." />
        </div>
        <div className="form-group">
          <button className="btn btn-primary" type="button" onClick={authorise}>Authorise Address</button>
        </div>
    </div>
  );
}
