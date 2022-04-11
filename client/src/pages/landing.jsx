import React from "react";
import Footer from './../components/footer';
import Navbar from './../components/navbar';
import LayerCollection from "../components/layers";
import Output from "../components/output";
import './style/content.css'

const Landing = () => {
    return (
        <>
            <Navbar/>
            <div className="content">
                <div className="row">
                    <LayerCollection />
                    <Output />
                </div>
            </div>
            <Footer/>
        </>
    );
};

export default Landing;