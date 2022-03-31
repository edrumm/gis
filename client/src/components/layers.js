import { useState } from 'react';
import { BiLayerMinus } from 'react-icons/bi';
import Upload from './upload';
import './style/layercollection.css';
import './style/layer.css';

const Layer = (props) => {

    const [selected, setSelected] = useState(false);
    const [BGColour, setBGColour] = useState('#eeeeee');

    const toggleSelect = () => {
        if (selected) {
            setSelected(false);
            setBGColour('#eeeeee');
            props.deselect(props.index);

        } else {
            setSelected(true);
            setBGColour('#4775e7'); // 1a4bc7
            props.select(props.index);
        }
    };

    const removeLayer = () => {
        setSelected(false);
        props.remove(props.index);
    };

    return(
        <>
        <div className="layer" style={{backgroundColor: BGColour}} onClick={toggleSelect}>
            <ul>
                <li className='layer-name'>{props.name}</li>
                <li className='layer-subtitle'>{props.type}</li>
                <li className='layer-subtitle'>{props.srid}</li>
            </ul> 
            <span className="rm-layer" onClick={removeLayer}>
                <BiLayerMinus/>
            </span>
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

    const MAX_LAYERS = 8;

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
                    layers.map((l, i) => (
                        <Layer 
                            name={l.name} 
                            type={l.type} 
                            srid={l.srid} 
                            index={i} 
                            select={selectLayer} 
                            deselect={deselectLayer}
                            remove={removeLayer}
                        />
                    ))
                }
            </div>
            <hr/>
            <Upload upload={uploadLayer}/>
        </div>
        </>
    );
};

export default LayerCollection;