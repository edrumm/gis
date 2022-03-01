import Map, {Marker, Source, Layer} from 'react-map-gl';
import 'mapbox-gl/dist/mapbox-gl.css';
import './style/map.css';

const MapWindow = () => {

    const MAPBOX_TOKEN = process.env.REACT_APP_MAPBOX_API_TOKEN;

    // TEST DATA
    const data = {
        type: 'FeatureCollection',
        features: [
          {type: 'Feature', geometry: {type: 'Point', coordinates: [-73.9299178, 40.813077]}}
        ]
    };

    const layerStyle = {
        id: 'subway stations',
        type: 'circle',
        paint: {
            'circle-radius': 5,
            'circle-color': '#007cbf'
        }
    };
    // ------------

    return (
        <>
            <Map
                initialViewState={{
                    longitude: -122.45,
                    latitude: 37.78,
                    zoom: 14
                }}                
                mapStyle="mapbox://styles/mapbox/streets-v9"
                mapboxAccessToken={MAPBOX_TOKEN}
            >
                <Source id="my-data" type="geojson" data={data}>
                    <Layer {...layerStyle} />
                </Source>
            </Map>
        </>
    )

};

export default MapWindow;