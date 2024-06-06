import React from "react";
import WindowFrame2 from "./window/WindowFrameV2";
import SubWindowFrame1 from "./subWindow/SubFrame1";
import SubWindowFrame2 from "./subWindow/SubFrame2"
import CircleButton from "./middlecircle/CircleButton";
import "./dashboard.css"
import DocumentUpload from "./documents/upload_doc";
import Documents from "./documents/Documents";

const Dashboard = () => {
    return (
        <div className="dashboard">
            <h1 className="dash-head">DOCUMENT MANAGEMENT SYSTEM</h1>

            <WindowFrame2 />
            <SubWindowFrame2 className="subframe2"/>
            <DocumentUpload className="upload" />

            <CircleButton className="circleButton"/>
            <Documents />
        </div>
    )
}

export default Dashboard;