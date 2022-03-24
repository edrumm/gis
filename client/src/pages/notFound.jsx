import React from 'react';
import Footer from './../components/footer';
import Navbar from './../components/navbar';
import './style/content.css';
import './style/error.css';

const NotFound = () => {
    return(
        <>
            <Navbar/>
            <div className="content">
                404
            </div>
            <Footer/>
        </>
    );
};

export default NotFound;
