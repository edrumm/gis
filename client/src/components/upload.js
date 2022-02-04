import { useState } from 'react';
import './style/upload.css';
import './layer';
import Layer from './layer';

const Upload = () => {

    // https://medium.com/excited-developers/file-upload-with-react-flask-e115e6f2bf99

    const [fileName, setFileName] = useState('');
    const [file, setFile] = useState('');

    const send = event => {
        event.preventDefault();
        
        const data = new FormData();
        data.append("file", file);
        data.append("filename", fileName);

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

    const test = event => {
        event.preventDefault();

        console.log(file.name);
        console.log(file);
    };

    return (
        <>
        <form className="upload-form" onSubmit={send}>
            <label>
                File:
                <input type="file" onChange={e => { 
                    setFile(e.target.files[0]);
                    setFileName(file.name);
                }} />
            </label>
            <br/>
            <input type="submit" value="Upload"/>
        </form>
        </>
    );
};

export default Upload;