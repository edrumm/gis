import React from "react";
import Footer from './../components/footer';
import Navbar from './../components/navbar';
import './style/content.css';

const Display = () => {
    return (
        <>
            <Navbar/>
            <div className="content">
                Content
            </div>
            <Footer/>
        </>
    )
};

export default Display;