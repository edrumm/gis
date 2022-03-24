import React from "react";
import Footer from './../components/footer';
import Navbar from './../components/navbar';
import './style/content.css'

const Landing = () => {
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

export default Landing;