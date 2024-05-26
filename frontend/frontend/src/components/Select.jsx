import React from 'react';
import axios from 'axios';


export default function Drop({selection,setRes,position}){

  const shorterHandle = () => {
    const data = {
      selected_text : selection,
      length_modification : "shorter"
    }
    axios.post("http://localhost:8000/regenerate", data ).then(function (response) {
      console.log(response);
      setRes(response);
      
    })
    .catch(function (error) {
      console.log(error);
    });
  }
  const longerHandle = () => {
    const data = {
      selected_text : selection,
      length_modification : "longer"
    }
    axios.post("http://localhost:8000/regenerate", data ).then(function (response) {
      console.log(response);
      setRes(response);
      
    })
    .catch(function (error) {
      console.log(error);
    });
  }

  return (
     <div style={{display : "flex", width : "80px",position : "absolute",flexDirection : "column", transform: `translate3d(${position.x}px, ${position.y}px, 0)`}}>
      <button onClick={shorterHandle} >Shorter</button>
      <button onClick={longerHandle} >Longer</button>
     </div>
  )
}