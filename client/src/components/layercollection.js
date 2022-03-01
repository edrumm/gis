import { useState } from 'react';
import Layer from './layer';
import './style/layercollection.css';

const LayerCollection = () => {

    const [layers, setLayers] = useState([]);

    const addLayer = () => {
        
    }

    return (
        <>
        <div className='layer-collection'>
            <ul>
                <li><Layer name="Locations" type="Vector" srid="26918"/></li>
                <li><Layer name="Elevation of city" type="Raster" srid="4326"/></li>
                <li><Layer name="MapBox" type="Base Map" srid="4326"/></li>
            </ul>
            
        </div>
        </>
    );
};

export default LayerCollection;