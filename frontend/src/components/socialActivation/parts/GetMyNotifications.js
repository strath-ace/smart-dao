//import React from "react";

export function GetMyNotifications({notifications}) {
    if (notifications !== undefined) {
        var _tr = document.createElement("tr");
        document.getElementById("notifications-table").innerHTML = "";
        for (let i = 0; i < notifications.length; i++) {
            _tr = document.createElement("tr");

            var _td1 = document.createElement("td");
            _td1.innerHTML = notifications[i].disaster_type;
            //_td1.appendChild(document.createTextNode())

            var _td2 = document.createElement("td");
            _td2.innerHTML = notifications[i].region;
            var _td3 = document.createElement("td");
            _td3.innerHTML = notifications[i].timestamp;

            var _td4 = document.createElement("td");
            var el = document.createElement("div");      
            _td4.appendChild(el);     

            _tr.appendChild(_td1);
            _tr.appendChild(_td2);
            _tr.appendChild(_td3);
            _tr.appendChild(_td4);

            document.getElementById("notifications-table").appendChild(_tr);
        }
    }
}
