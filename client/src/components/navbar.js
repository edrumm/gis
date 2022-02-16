import { useState } from 'react';
import './style/navbar.css';

const Navbar = () => {
    return(
        <>
        <nav>
            <ul>
                <li id='dropdown-icon'>☰</li>
                <li>Online GIS</li>
                <li>Navbar 1</li>
                <li>Navbar 2</li>
            </ul>
        </nav>
        </>
    );
};

export default Navbar;