import { useState } from 'react';
import './style/upload.css';
import './layer';
import Layer from './layer';

const Upload = () => {

    // https://medium.com/excited-developers/file-upload-with-react-flask-e115e6f2bf99

    const [fileName, setFile] = useState('');

    const send = event => {
        event.preventDefault();
        // Handle upload

        const data = {
            filename: fileName
        };

        const options = {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        };

        fetch('/upload', options)
        .then(res => res.json())
        .then(json => console.log(json.body)) // placeholder, save returned geom
        .catch(err => console.error(err)) // placeholder, output error to interface
    };

    return (
        <>
        <form class="upload-form" onSubmit={send}>
            <label>
                File:
                <input type="file" onChange={e => setFile(e.target.value)}/>
            </label>
            <br/>
            <input type="submit" value="Upload"/>
        </form>
        </>
    );
};

export default Upload;