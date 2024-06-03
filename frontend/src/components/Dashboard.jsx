import React from "react";
import WindowFrame2 from "./window/WindowFrameV2";
import RoundIcon1 from "./icons/RoundIcon1";
import SubWindowFrame1 from "./subWindow/SubFrame1";
import SubWindowFrame2 from "./subWindow/SubFrame2"
import "./dashboard.css"

const Dashboard = () => {
    return (
        <div className="dashboard">
            <WindowFrame2 />
            <h1>DOCUMENT MANAGEMENT SYSTEM</h1>
           
            <SubWindowFrame2 className="subframe2"/>
            <p className="first">hello world</p>
            <p className="second">Building on progress</p>
        </div>
    )
}

export default Dashboard;