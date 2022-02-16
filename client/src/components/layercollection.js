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
            Layer Collection
        </div>
        </>
    );
};

export default LayerCollection;