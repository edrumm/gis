import { GoFileBinary } from 'react-icons/go';
import { BiShapePolygon, BiHome } from 'react-icons/bi';
import { error, success } from './popup';
import { vector, raster } from '../request';
import './style/navbar.css';

const openPage = (url) => {
    window.open(url, '_blank');
};

// https://blog.logrocket.com/creating-multilevel-dropdown-menu-react/
const Submenu = (props) => {
    return (
        <>
        <ul className='submenu'>
            {props.menu.map((p, i) => {
                if (typeof p.action === "function")
                {
                    return (
                        <li key={i} onClick={() => p.action()}>
                            {p.title}
                        </li>
                    );
                }

                return (
                    <li key={i} onClick={() => openPage(p.action)}>
                        {p.title}
                    </li>
                );
            })
        }
        </ul>
        </>
    );
};

const Items = (props) => {
    return (
        <li>
        {
            <>
            {props.item.title}
            <Submenu menu={props.item.submenu} selectedLayers={props.selectedLayers}/>
            </>
        }
        </li>
    );
};

const Navbar = (props) => {

    const pointsInPolygon = () => {

        if (props.selectedLayers.length !== 2) {
            error('Points-in-polygon requires 2 layers');
            return;
        }

        const points = props.selectedLayers[0];
        const polygon = props.selectedLayers[1];

        if (points.type !== 'Vector' || polygon.type !== 'Vector') {
            error('Points-in-polygon cannot be performed on raster layers');
            return;

        } else if (points.srid !== polygon.srid) {
            error('Points-in-polygon cannot be performed across different SRIDs');
            return;
        }

        success(`Computing Points-in-Polygon of ${points.name}, ${polygon.name}`);

        vector('points-in-polygon', [points, polygon], props.setGeom);

        props.setRaster(null);
        props.setOutputType(null);
    };
    
    const voronoiPolygons = () => {
        if (props.selectedLayers.length !== 1) {
            error('Voronoi Polygons requires 1 layer');
            return;
        }

        const points = props.selectedLayers[0];

        if (points.type !== 'Vector') {
            error('Voronoi Polygons cannot be performed on a raster layer');
            return;
        }

        success(`Computing Voronoi Polygons of ${points.name}`);

        vector('voronoi polygons', [points], props.setGeom);

        props.setRaster(null);
        props.setOutputType('vector');
    };
    
    const convexHull = () => {
        if (props.selectedLayers.length !== 1) {
            error('Convex Hull requires 1 layer');
            return;
        }

        const points = props.selectedLayers[0];

        if (points.type !== 'Vector') {
            error('Convex Hull cannot be performed on a raster layer');
            return;
        }

        success(`Computing Convex Hull of ${points.name}`);

        vector('convex hull', [points], props.setGeom);

        props.setRaster(null);
        props.setOutputType('vector');
    };
    
    const slope = () => {
        if (props.selectedLayers.length !== 1) {
            error('Slope requires 1 layer');
            return;
        }

        const file = props.selectedLayers[0];

        if (file.type !== 'Raster') {
            error('Slope cannot be performed on a vector layer');
            return;
        }

        success(`Computing Slope of ${file.name}`);

        raster('slope', file, props.setRaster);

        props.setGeom({});
        props.setOutputType('raster');
    };
    
    const aspect = () => {
        if (props.selectedLayers.length !== 1) {
            error('Aspect requires 1 layer');
            return;
        }

        const file = props.selectedLayers[0];

        if (file.type !== 'Raster') {
            error('Aspect cannot be performed on a vector layer');
            return;
        }

        success(`Computing Aspect of ${file.name}`);

        raster('aspect', file, props.setRaster);

        props.setGeom({});
        props.setOutputType('raster');
    };

    const items = [
        {
            title: <BiHome/>,
            submenu: [
                { title: 'GitHub', action: 'https://github.com/edrumm/gis' },
                { title: 'Heriot-Watt University', action: 'https://www.hw.ac.uk/' }
            ]
        },
        {
            title: <BiShapePolygon/>,
            submenu: [
                { title: 'Points in polygon', action: pointsInPolygon },
                { title: 'Convex Hull', action: convexHull },
                { title: 'Voronoi Polygon', action: voronoiPolygons }
            ]
        },
        {
            title: <GoFileBinary/>,
            submenu: [
                { title: 'DEM Slope', action: slope },
                { title: 'DEM Aspect', action: aspect }
            ]
        }
    ];

    return(
        <>
        <div className='container'>
            <header>
                <nav className='navbar'>
                    <ul className='navbar-ul'>
                        {
                            items.map((item, i) => {
                                return (
                                    <Items 
                                        item={item} 
                                        key={i} 
                                        selectedLayers={props.selectedLayers}
                                    />
                                );
                            })
                        }
                    </ul>
                </nav>
            </header>
        </div>
        </>
    );
};

export default Navbar;