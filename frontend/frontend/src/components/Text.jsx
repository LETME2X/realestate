import React, { useEffect, useState } from 'react';
import Select from './Select';
import './Text.css';

export default function Text({ res, setRes, isLoading }) {
    const [selection, setSelection] = useState("");
    const [position, setPosition] = useState({});

    useEffect(() => {
        const handleSelectionChange = () => {
            const activeSelection = document.getSelection();
            const text = activeSelection?.toString();

            if (!activeSelection || !text) {
                setSelection(undefined);
                return;
            }

            setSelection(text);

            const rect = activeSelection.getRangeAt(0).getBoundingClientRect();

            setPosition({
                x: rect.left + (rect.width / 2) - 350,
                y: rect.top + window.scrollY - 290,
                width: rect.width,
                height: rect.height,
            });
        };

        document.addEventListener('selectionchange', handleSelectionChange);

        return () => {
            document.removeEventListener('selectionchange', handleSelectionChange);
        };
    }, []);

    return (
        <div>
            {selection && <Select setRes={setRes} selection={selection} position={position} />}
            <p>{isLoading ? <span>Loading...</span> : res}</p>
        </div>
    );
}
