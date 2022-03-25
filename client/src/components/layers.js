import { useState } from 'react';
import { BiLayerMinus } from 'react-icons/bi';
import Upload from './upload';
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
            {/* <span class="rm-layer">
                <BiLayerMinus/>
            </span> */}
        </div>
        </>
    );
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

    const [selectedLayers, setSelectedLayers] = useState([]);

    const uploadLayer = (name, type, srid) => {
        let newLayer = { name: name, type: type, srid: srid };
        let layerList = [...layers, newLayer];

        setLayers(layerList);
    };

    const selectLayer = i => {
        let selected = [...selectedLayers];
        let allLayers = [...layers];

        selected.push(allLayers[i]);
        setSelectedLayers(selected);
    };

    const deselectLayer = i => {
        let selected = [...selectedLayers];

        selected.pop(i);
        setSelectedLayers(selected);
    };

    const removeLayer = i => {
        let layerList = [...layers];
        layerList.splice(i, 1);

        setLayers(layerList);
    };

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
            <hr/>
            <Upload/>
        </div>
        </>
    );
};

export default LayerCollection;