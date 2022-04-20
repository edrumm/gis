import Map, {Marker, Source, Layer} from 'react-map-gl';
import 'mapbox-gl/dist/mapbox-gl.css';
import './style/map.css';

const MAPBOX_TOKEN = process.env.REACT_APP_MAPBOX_API_TOKEN;

const MapWindow = (props) => {

    const layerStyle = {
        id: 'geom',
        type: 'fill',
        paint: {
            'fill-color': 'rgba(71, 113, 231, 0.4)',
            'fill-outline-color': '#4775e7'
        }
    };

    return (
        <>
            <Map               
                mapStyle="mapbox://styles/mapbox/streets-v9"
                mapboxAccessToken={MAPBOX_TOKEN}
            >
                <Source id="my-data" type="geojson" data={props.geom}>
                    <Layer {...layerStyle} />
                </Source>
            </Map>
        </>
    )

};

export default MapWindow;