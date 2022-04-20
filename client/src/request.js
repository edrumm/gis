import { success, error } from "./components/popup";

const downloadBlob = (name) => {
    const data = {
        filename: name
    };

    const options = {
        method: 'POST',
        mode: 'cors',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    };

    // https://stackoverflow.com/questions/54542776/saving-file-from-blobhttp-using-javascript-with-no-redirection
    fetch('/download', options)
    .then(response => response.blob())
    .then(blob => {
        const URL = window.URL || window.webkitURL;
        const blobUrl = URL.createObjectURL(blob);

        const link = document.createElement('a');

        if (typeof link.download === 'undefined') {
            window.location = blobUrl;

        } else {
            link.href = blobUrl;
            link.download = name;

            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        }
    })
    .catch(err => error(err));
}

const vector = (type, layers, setGeom) => {
    let body = {
        points: layers[0].name.substring(0, layers[0].name.lastIndexOf('.'))
    };

    let route;

    if (type === 'points-in-polygon') {
        body.polygon = layers[1].name.substring(0, layers[1].name.lastIndexOf('.'));
        route = '/count';

    } else if (type === 'convex hull') {
        route = '/convex';

    } else {
        route = '/voronoi';
    }

    const options = {
        method: 'POST',
        mode: 'cors',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(body)
    };

    fetch(route, options)
    .then(response => response.json())
    .then(json => {
        const geom = JSON.parse(json.body);

        if (json.err) {
            error(json.err);
        } else {
            if (type !== 'points-in-polygon') {
                setGeom(geom);
            }

            success('Analysis complete');
            downloadBlob(json.filename);
        }
    })
    .catch(err => {
        error(err);
    });
};

const raster = (type, layer, setRaster) => {
    const body = {
        file: layer.name
    };

    const options = {
        method: 'POST',
        mode: 'cors',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(body)
    };

    let route;

    if (type === 'slope') {
        route = '/slope';

    } else {
        route = '/aspect';
    }

    fetch(route, options)
    .then(response => response.blob())
    .then(blob => {
        if (!blob) {
            error('Something went wrong');

        } else {
            success('Analysis complete');

            const url = URL.createObjectURL(blob);
            setRaster(url);

            const zipName = `${layer.name.substring(0, layer.name.lastIndexOf('.'))}-${type}.zip`;
            downloadBlob(zipName);
        }
    })
    .catch(err => {
        error(err);
    });
};

export { vector, raster };