import { useState } from 'react';
import './style/upload.css';

const Upload = () => {

    // https://medium.com/excited-developers/file-upload-with-react-flask-e115e6f2bf99

    const [fileName, setFile] = useState(null);
    const [format, setFormat] = useState(null); // maybe

    const send = event => {

    };

    return (
        <>
        <form class="upload-form" onSubmit={send}>
            <label>
                File:
                <input type="text" onChange={e => setFile(e.target.value)}/>
            </label>
            <br/>
            <input type="submit" value="Upload"/>
        </form>
        </>
    );
};

export default Upload;