import './style/output.css';
import { useEffect } from 'react';
import MapWindow from './map';

const Output = (props) => {

    useEffect(() => {
        console.log(props.raster);
    }, [props.raster]);

    if (props.outputType === 'vector') { 

        if (!props.geom) {
            return (
                <>
                <div className="output">
                    Perform analysis to display an output
                </div>
                </>
            );
        }

        return (
            <>
            <div className="output">
                <MapWindow geom={props.geom}/>
            </div>
            </>
        );
    } else if (props.outputType === 'raster') {

        if (!props.raster) {
            return (
                <>
                <div className="output">
                    Perform analysis to display an output
                </div>
                </>
            );
        }

        return (
            <>
            <div className="output">
                <img className='raster-image' src={props.raster} alt='Raster image'></img>
            </div>
            </>
        );
    } else {
        return (
            <>
            <div className="output">
                Perform analysis to display an output
            </div>
            </>
        );
    }
};

export default Output;