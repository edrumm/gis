import React, { useState } from "react";
import Footer from './../components/footer';
import Navbar from './../components/navbar';
import LayerCollection from "../components/layers";
import Output from "../components/output";
import './style/content.css'

const Landing = () => {
    
    const [layers, setLayers] = useState([]);

    const [selectedLayers, setSelectedLayers] = useState([]);

    const [geom, setGeom] = useState({});

    const [raster, setRaster] = useState(null);

    const [outputType, setOutputType] = useState(null);

    const uploadLayer = (name, type, srid) => {
        let newLayer = { name: name, type: type, srid: srid };
        let layerList = [...layers, newLayer];

        setLayers(layerList);
    };

    return (
        <>
            <Navbar 
                setGeom={setGeom} 
                setRaster={setRaster} 
                setOutputType={setOutputType} 
                selectedLayers={selectedLayers} 
                uploadLayer={uploadLayer}
            />
            <div className="content">
                <div className="row">
                    <LayerCollection 
                        layers={layers}
                        setLayers={setLayers}
                        selectedLayers={selectedLayers}
                        setSelectedLayers={setSelectedLayers}
                        uploadLayer={uploadLayer}
                    />
                    <Output geom={geom} raster={raster} outputType={outputType}/>
                </div>
            </div>
            <Footer/>
        </>
    );
};

export default Landing;