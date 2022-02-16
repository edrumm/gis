import { useState } from 'react';
import './style/layer.css';

const Layer = (props) => {

    return(
        <>
        <div className="layer">

            <ul>
                <li className='layer-name'>{props.name}</li>
                <li className='layer-subtitle'>{props.type}</li>
                <li className='layer-subtitle'>{props.srid}</li>
            </ul>
            
        </div>
        </>
    );
};

// Create layer
// <Layer name="Locations" type="Vector" srid="26918"/>
// <Layer name="Elevation of city" type="Raster" srid="4326"/>

export default Layer;