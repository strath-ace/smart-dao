//import React from "react";

export function GetDisasters({disasters}) {
    if (disasters !== undefined) {
        var _tr = document.createElement("tr");
        document.getElementById("disasters-table").innerHTML = "";
        for (let i = 0; i < disasters.length; i++) {
            _tr = document.createElement("tr");

            var _td1 = document.createElement("td");
            _td1.innerHTML = disasters[i].disaster_type;
            //_td1.appendChild(document.createTextNode())

            var _td2 = document.createElement("td");
            _td2.innerHTML = disasters[i].region;
            var _td3 = document.createElement("td");
            _td3.innerHTML = disasters[i].time_of_first_notification;
            var _td4 = document.createElement("td");
            _td4.innerHTML = disasters[i].time_of_consensus;

            var _td5 = document.createElement("td");
            var el = document.createElement("div");      
            _td5.appendChild(el);     

            _tr.appendChild(_td1);
            _tr.appendChild(_td2);
            _tr.appendChild(_td3);
            _tr.appendChild(_td4);
            _tr.appendChild(_td5);

            document.getElementById("disasters-table").appendChild(_tr);
        }
    }
}
