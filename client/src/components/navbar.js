import { SiMapbox } from 'react-icons/si';
import { GoFileBinary } from 'react-icons/go';
import { BiLayerPlus, BiShapePolygon, BiCog } from 'react-icons/bi';
import { AiOutlineDownload } from 'react-icons/ai';
import './style/navbar.css';

// https://blog.logrocket.com/creating-multilevel-dropdown-menu-react/
const items = [
    {
        title: 'Online GIS',
        submenu: [
            { title: 'GitHub' },
            { title: 'Heriot-Watt University' }
        ]
    },
    {
        title: <BiShapePolygon/>,
        submenu: [
            { title: 'Points in polygon' },
            { title: 'Convex Hull' },
            { title: 'Voronoi Polygon' }
        ]
    },
    {
        title: <GoFileBinary/>,
        submenu: [
            { title: 'DEM Slope' },
            { title: 'DEM Aspect' }
        ]
    },
    {
        title: <BiCog/>,
        submenu: [
            { title: 'Clear All Layers' }
        ]
    }
];

const Submenu = ({ props }) => {

    return (
        <ul className='submenu'>
            {props.map((p, i) => {
                return (
                    <li key={i}>
                        {p.title}
                    </li>
                );
            })
        }
        </ul>
    );
};

const Items = ({ props }) => {
    return (
        <li>
        {
            <>
            {props.title}
            <Submenu props={props.submenu} />
            </>
        }
        </li>
    );
};

const Navbar = () => {
    return(
        <>
        <div className='container'>
            <header>
                <nav className='navbar'>
                    <ul className='navbar-ul'>
                        {
                            items.map((item, i) => {
                                return (
                                    <Items props={item} key={i} />
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