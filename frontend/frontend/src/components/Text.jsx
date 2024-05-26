import React from 'react';
import { useEffect,useState } from 'react';
import Drop from './Select';
import './Text.css';

export default function Regenerate({res,setRes,isLoading}){

    const [selection, setSelection] = useState("");
    
    const [position, setPosition] = useState({});
   
    useEffect(() => {
      document.addEventListener('selectionchange', () => {
        const activeSelection = document.getSelection();
        const text = activeSelection?.toString();
    
        if ( !activeSelection || !text ) {
          setSelection(undefined);
          return;
        };
    
        setSelection(text);
    
        const rect = activeSelection.getRangeAt(0).getBoundingClientRect()
    
        setPosition({
          // 80 represents the width of the share button, this may differ for you
          x: rect.left + (rect.width / 2) - 350 ,
          // 30 represents the height of the share button, this may differ for you
          y: rect.top + window.scrollY - 290,
          width: rect.width,
          height: rect.height,
        })
      });
    }, []);

    return(
        <div >
            {selection && <Drop setRes={setRes} selection={selection} position={position}/>}
            <p>{isLoading ? <span>Loading...</span> : res}</p>
        </div>
    )


}