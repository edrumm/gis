import { useState } from 'react';
import './style/layercollection.css';
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

const UploadLayer = (props) => {

};

const LayerCollection = () => {

    const [layers, setLayers] = useState([{
        name: 'nyc_neighborhoods',
        type: 'Vector',
        srid: 26918
    }, {
        name: 'nyc_subway_stations',
        type: 'Vector',
        srid: 26918
    }]);

    return (
        <>
        <div className='layer-collection'>
            <div className='layer-header'>Upload Layers</div>
            <div className='layer-list'>
                {
                    layers.map(l => (
                        <Layer name={l.name} type={l.type} srid={l.srid}/>
                    ))
                }
            </div>
        </div>
        </>
    );
};

export default LayerCollection;