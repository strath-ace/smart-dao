import React from "react";

export function NewNotification({new_notification, confirm_consensus}) {

  function notification() {
    var _type = document.getElementById("type_box");
    var _regions = document.getElementById("regions_box");
    if (_type.value === "" || _regions.value === "") {
      console.log("Empty Type or Regions of Disaster");
    } else {
      new_notification(_type.value, [_regions.value]);
    }
  }

  function consensus() {
    var _type = document.getElementById("type_box");
    var _regions = document.getElementById("regions_box");
    if (_type.value === "" || _regions.value === "") {
      console.log("Empty Type or Regions of Disaster");
    } else {
      confirm_consensus(_type.value, [_regions.value]);
    }
  }

  return (
    <div>
      <h4>Disaster Data</h4>
        
        <div className="form-group">
          <label>Type of Disaster</label>
          <input id="type_box" className="form-control" step="1" name="_type" placeholder="0 to 5" />
        </div>
        <div className="form-group">
          <label>Regions (If multiple, seperate with comma)</label>
          <input id="regions_box" className="form-control" step="1" name="_region" placeholder="0 to 360*180" />
        </div>
        <div className="form-group">
          {/* <input className="btn btn-primary" type="button" id="notification_button" value="Create Notification" onclick={notification();}/>
          <input className="btn btn-primary" type="button" id="consensus_button" value="Confirm Consensus" onclick="consensus();"/> */}
          <button className="btn btn-primary" type="button" onClick={notification}>New Notification</button>
          <button className="btn btn-primary" type="button" onClick={consensus}>Confirm Consensus</button>
        </div>
    </div>
  );
}
