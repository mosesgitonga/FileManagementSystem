import React from "react";
import WindowFrame2 from "./window/WindowFrameV2";
import RoundIcon1 from "./icons/RoundIcon1";
import SubWindowFrame1 from "./subWindow/SubFrame1";
import SubWindowFrame2 from "./subWindow/SubFrame2"
import CircleButton from "./middlecircle/CircleButton";
import "./dashboard.css"

const Dashboard = () => {
    return (
        <div className="dashboard">
            <h1 class="dash-head">DOCUMENT MANAGEMENT SYSTEM</h1>

            <WindowFrame2 />
            <SubWindowFrame2 className="subframe2"/>
            <CircleButton className="circleButton"/>
            

        </div>
    )
}

export default Dashboard;