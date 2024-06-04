import React from "react";
import './CircleButton.css';

const CircleButton = () => {
    const handleClick = () => {
        // Specify the URL you want to open in the pop-up window
        const url = "https://www.google.com";
        // Specify the features of the pop-up window
        const features = "width=600,height=400,resizable=yes,scrollbars=yes,status=yes";
        // Open the pop-up window
        window.open(url, "_blank", features);
    };

    return (
        <div className="circleButton">
            <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;700&display=swap" rel="stylesheet" />
            <svg width="400" height="400" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="none">
                <circle cx="200" cy="200" r="160" fill="none" stroke="#00d9ff" strokeWidth="5" strokeDasharray="4,4" />
                <circle className="glow" cx="200" cy="200" r="150" fill="#00d9ff" stroke="black" strokeWidth="15" strokeDasharray="4, 4" />
                <circle cx="200" cy="200" r="125" stroke="black" strokeWidth="2" fill="black" />
                <circle className="glow" cx="200" cy="200" r="120" stroke="#00d9ff" strokeWidth="2" fill="#00d9ff" />
                <circle cx="200" cy="200" r="115" stroke="black" strokeWidth="2" fill="black" />
                <circle className="glow" cx="200" cy="200" r="106" stroke="#00d9ff" strokeWidth="0.6" fill="#00d9ff" />
                <circle cx="200" cy="200" r="112" fill="#00d9ff" stroke="black" strokeWidth="30" strokeDasharray="4, 4" />

                {/* Overlaying HTML button */}
                <foreignObject x="150" y="150" width="100" height="100">
                    <button className="innerButton" onClick={handleClick}>
                        <circle cx="200" cy="200" r="105" stroke="cyan" strokeWidth="2" />
                        <text x="145" y="210" width="50" height="40" fill="none" fontSize="12" fontWeight="bold">Manage System</text>
                    </button>
                </foreignObject>
            </svg>
        </div>
    );
};

export default CircleButton;
