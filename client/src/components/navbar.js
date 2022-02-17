import { FaVectorSquare, FaRegMap } from 'react-icons/fa';
import { GoFileBinary } from 'react-icons/go';
import { BiLayerPlus, BiLayerMinus, BiShapePolygon, BiCog } from 'react-icons/bi';
import { AiOutlineDownload, AiOutlineUpload } from 'react-icons/ai';
import './style/navbar.css';

// https://stackoverflow.com/questions/60877944/react-how-to-pass-an-array-as-props-and-render-a-list-of-images
const Submenu = (props) => {
    return (
        <ul className='submenu'>
            
        </ul>
    );
};

const Navbar = () => {
    return(
        <>
        <nav>
            <ul>
                <li id='dropdown-icon'>☰</li>
                <li><BiShapePolygon/></li>
                <li><GoFileBinary/></li>
                <li><BiLayerPlus/></li>
                <li><AiOutlineDownload/></li>
                <li><FaRegMap/></li>
                <li><BiCog/></li>
            </ul>
        </nav>
        </>
    );
};

export default Navbar;