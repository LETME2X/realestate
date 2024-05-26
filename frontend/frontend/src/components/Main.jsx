import React, { useState } from "react";
import Text from './Text';
import Select from 'react-select';
import axios from 'axios';
import './Main.css';

function Main() {
    const [length, setLength] = useState({ value: "Select", label: "Select" });
    const [tone, setTone] = useState({ value: "Select", label: "Select" });
    const [features, setFeautures] = useState("");
    const [brandPos, setBrandPos] = useState("");
    const [res, setRes] = useState("");
    const [isLoading, setIsLoading] = useState(false);
    const [insertLoader, setInsertLoader] = useState(false);

    const lengthOptions = [
        { value: "Short", label: "Short" },
        { value: "Medium", label: "Medium" },
        { value: "Long", label: "Long" }
    ];

    const toneOptions = [
        { value: "Casual", label: "Casual" },
        { value: "Formal", label: "Formal" },
        { value: "Grandiose", label: "Grandiose" }
    ];

    const featuresList = features.split(',');

    const toneChange = (val) => {
        setTone(val);
    };
    const lengthChange = (val) => {
        setLength(val);
    };

    const generateHandler = async () => {
        setIsLoading(true);
        const data = {
            features: featuresList,
            tone: tone.label,
            length: length.label,
            brand_positioning: brandPos
        };

        try {
            const response = await axios.post("http://localhost:8000/generate", data);
            console.log(response);
            setRes(response.data.generated_copy);
            setIsLoading(false);
        } catch (error) {
            console.log(error);
            setIsLoading(false);
        }
    };

    const insertInDB = async () => {
        setInsertLoader(true);
        const data = {
            features: featuresList,
            tone: tone.label,
            length: length.label,
            brand_positioning: brandPos,
            output: res
        };

        try {
            const response = await axios.post("http://localhost:8000/insert", data);
            console.log(response);
            setInsertLoader(false);
        } catch (error) {
            console.log(error);
            setInsertLoader(false);
        }
    };

    const regenerateHandler = async (modificationType) => {
        const data = {
            complete_text: res,
            selected_text: window.getSelection().toString(),
            length_modification: modificationType
        };
    
        try {
            const response = await axios.post("http://localhost:8000/regenerate", data);
            setRes(response.data.regenerated_copy);
        } catch (error) {
            console.error(error);
        }
    };
    

    const handleContextMenu = (event) => {
        event.preventDefault();
        const menu = document.getElementById("context-menu");
        menu.style.top = `${event.clientY}px`;
        menu.style.left = `${event.clientX}px`;
        menu.style.display = "block";
    };

    const handleClick = () => {
        const menu = document.getElementById("context-menu");
        if (menu.style.display === "block") {
            menu.style.display = "none";
        }
    };

    return (
        <div className="App" onClick={handleClick}>
            <div className="container">
                <div className="sub-container">
                    <div className="element">
                        <span>Brand Positioning</span>
                        <input value={brandPos} onChange={(e) => { setBrandPos(e.target.value) }} style={{ padding: "10px" }} placeholder="text" />
                    </div>
                    <div className="element">
                        <span>Features</span>
                        <input value={features} onChange={(e) => { setFeautures(e.target.value) }} style={{ padding: "10px" }} placeholder="text" />
                    </div>
                </div>
                <div className="sub-container">
                    <div className="element">
                        <span>Tone</span>
                        <Select options={toneOptions} value={tone} onChange={toneChange} />
                    </div>
                    <div className="element">
                        <span>Length</span>
                        <Select options={lengthOptions} value={length} onChange={lengthChange} />
                    </div>
                </div>
                <div className="btn">
                    <button onClick={generateHandler}>Generate</button>
                </div>
                <div className="output" onContextMenu={handleContextMenu}>
                    <span>Output</span>
                    <Text res={res} setRes={setRes} isLoading={isLoading} />
                </div>
                <div className="db-btn">
                    <button onClick={insertInDB}> {insertLoader ? <span>Loading...</span> : <span>Insert In DB</span>}</button>
                </div>
            </div>
            <div id="context-menu" className="context-menu">
                <div onClick={() => regenerateHandler("shorter")}>Shorter</div>
                <div onClick={() => regenerateHandler("longer")}>Longer</div>
            </div>
        </div>
    );
}

export default Main;
