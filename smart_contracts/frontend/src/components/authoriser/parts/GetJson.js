import React,{useState,useEffect} from 'react';

//import './App.css';

export function GetJson({get_json}) {
    const [data,setData]=useState([]);
    const getData=()=>{
        fetch('./data/network.config.json'
        ,{
        headers : { 
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        }
        )
        .then(function(response){
            //console.log(response)
            return response.json();
        })
        .then(function(myJson) {
            //console.log(myJson);
            setData(myJson)
        });
    }

    useEffect(()=>{
        getData()
        
    },[])
        
    get_json(data)

    // return (
    //     <div className="JsonData">
    //     {
    //     data.network.url// && data.length>0 && data.map((item)=><p>{item.network.url}</p>)
    //     }
    //     </div>
    // );

    //console.log(data);

    
}
