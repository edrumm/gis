import { useState } from 'react';
import './style/upload.css';
import Swal from 'sweetalert2';
// import Layer from './layer';

const Upload = () => {

    const [file, setFile] = useState(null);

    const Popup = Swal.mixin({
        toast: true,
        position: 'top-end',
        showConfirmButton: false,
        timer: 3000,
        timerProgressBar: true
    });

    const send = event => {
        event.preventDefault();

        if (file == null) {
            Popup.fire({
                title: 'No file selected',
                icon: 'error',
            });
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
                Popup.fire({
                    title: json.err,
                    icon: 'error',
                });
            } else {
                Popup.fire({
                    title: 'File uploaded',
                    icon: 'success',
                });
            }
        }) // placeholder, save returned geom
        .catch(err => {
            Popup.fire({
                title: err,
                icon: 'error',
            });
        });
    };

    const supportedTypes = '.shp, .zip, .geojson, .tiff, .tif, .bil';

    // VERY rough interface to test
    // will fix later
    return (
        <>
        <form className="upload-form" onSubmit={send}>
            <label>
                Upload<br/>
                <input type="file" accept={supportedTypes} name="file" onChange={e => { 
                    setFile(e.target.files[0]);
                }}/>
            </label>
            <br/>
            <input className='submit-button' type="submit" value="Upload"/>
        </form>
        </>
    );
};

export default Upload;