import { useState } from 'react';
import './style/upload.css';
import Swal from 'sweetalert2';
// import Layer from './layer';

const Upload = (props) => {

    const [file, setFile] = useState(null);
    const [srid, setSRID] = useState('3857');

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

        if (!srid.match(/^[0-9]+$/) || srid === '') {
            Popup.fire({
                title: 'Invalid SRID',
                icon: 'error',
            });
            return;
        }
        
        const data = new FormData();
        data.append("file", file);
        data.append("srid", srid);

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

                if (file.name.includes('.tif')) {
                    props.upload(file.name, 'Raster', 'None');
                } else {
                    props.upload(file.name, 'Vector', srid);
                }
            }
        })
        .catch(err => {
            Popup.fire({
                title: err,
                icon: 'error',
            });
        });
    };

    const supportedTypes = '.shp, .zip, .geojson, .tif';

    return (
        <>
        <form className="upload-form" onSubmit={send}>
            <label>
                Upload Layer <br/>
                <input type="file" accept={supportedTypes} name="file" onChange={e => { 
                    setFile(e.target.files[0]);
                }}/>
            </label>
            <label>
                <br/>
                SRID <br/>
                <input type="text" name="srid" onChange={e => {
                    setSRID(e.target.value.toString());
                }}/>
            </label>
            <br/>
            <input className='submit-button' type="submit" value="Upload"/>
        </form>
        </>
    );
};

export default Upload;