import { useState } from 'react';
import { MdOutlineCheckBox, MdOutlineIndeterminateCheckBox } from 'react-icons/md';
import { BiLayerMinus } from 'react-icons/bi';
import Upload from './upload';
import './style/layercollection.css';
import './style/layer.css';
import { error, success } from './popup';

const Layer = (props) => {

    const [selected, setSelected] = useState(false);
    const [BGColour, setBGColour] = useState('#eeeeee');

    const drop = () => {
        console.log(`Drop ${props.name}`);
    };

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

        drop();
    };

    if (selected) {
        return(
            <>
            <div className="layer" style={{backgroundColor: BGColour}}>
                <ul>
                    <li className='layer-name' key={0}>{props.name}</li>
                    <li className='layer-subtitle' key={1}>{props.type}</li>
                    <li className='layer-subtitle' key={2}>{props.srid}</li>
                    <li className='layer-options' key={3}>
                        <span onClick={removeLayer}>
                            <BiLayerMinus/>
                        </span>
                        &nbsp;
                        <span onClick={toggleSelect}>
                            <MdOutlineIndeterminateCheckBox/>
                        </span>
                    </li>
                </ul> 
            </div>
            </>
        );
    }

    return(
        <>
        <div className="layer" style={{backgroundColor: BGColour}}>
            <ul>
                <li className='layer-name' key={0}>{props.name}</li>
                <li className='layer-subtitle' key={1}>{props.type}</li>
                <li className='layer-subtitle' key={2}>{props.srid}</li>
                <li className='layer-options' key={3}>
                    <span onClick={removeLayer}>
                        <BiLayerMinus/>
                    </span>
                    &nbsp;
                    <span onClick={toggleSelect}>
                        <MdOutlineCheckBox/>
                    </span>
                </li>
            </ul> 
        </div>
        </>
    );
};

const LayerCollection = (props) => {

    const selectLayer = i => {
        let selected = [...props.selectedLayers];
        let allLayers = [...props.layers];

        selected.push(allLayers[i]);
        props.setSelectedLayers(selected);
    };

    const deselectLayer = i => {
        let selected = [...props.selectedLayers];

        selected.pop(i);
        props.setSelectedLayers(selected);
    };

    const removeLayer = i => {
        let layerList = [...props.layers];
        let selected = [...props.selectedLayers];

        const data = {
            filename: layerList[i].name
        };

        const options = {
            method: 'POST',
            mode: 'cors',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        };

        fetch('/drop', options)
        .then(response => response.json())
        .then(json => {

            if (json.body) {

                for (let i = 0; i < selected.length; i++) {
                    if (selected[i].name === layerList[i].name) {
                        deselectLayer(i);
                    }
                }
        
                layerList.splice(i, 1);
                props.setLayers(layerList);

                success('Layer removed');

            } else {
                error(json.err);
            }
        })
        .catch(err => error(err));
    };

    return (
        <>
        <div className='layer-collection'>
            <div className='layer-header'>Layers</div>
            <div className='layer-list'>
                {
                    props.layers.map((l, i) => (
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
            <Upload upload={props.uploadLayer}/>
        </div>
        </>
    );
};

export default LayerCollection;