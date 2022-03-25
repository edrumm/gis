import React from "react";
import Footer from './../components/footer';
import Navbar from './../components/navbar';
import LayerCollection from "../components/layers";
import './style/content.css'

const Landing = () => {
    return (
        <>
            <Navbar/>
            <div className="content">
                <LayerCollection />
            </div>
            <Footer/>
        </>
    );
};

export default Landing;