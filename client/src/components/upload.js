import { useState } from 'react';
import './style/upload.css';
import './layer';
import Layer from './layer';

const Upload = () => {

    const [file, setFile] = useState(null);

    const send = event => {
        event.preventDefault();

        if (file == null) {
            return;
        }
        
        const data = new FormData();
        data.append("file", file);

        const options = {
            method: 'POST',
            body: data
        };

        fetch('/upload', options)
        .then(res => res.json())
        .then(json => {
            if (json.err) {
                console.error(json.err);
            } else {
                console.log(json.body);
            }
        }) // placeholder, save returned geom
        .catch(err => console.error(err)) // placeholder, output error to interface
    };

    // VERY rough interface to test
    // will fix later
    return (
        <>
        <form className="upload-form" onSubmit={send}>
            <label>
                File:
                <input type="file" onChange={e => { 
                    setFile(e.target.files[0]);
                }} />
            </label>
            <br/>
            <input type="submit" value="Upload"/>
        </form>
        </>
    );
};

export default Upload;