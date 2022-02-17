import { FaVectorSquare, FaRegMap } from 'react-icons/fa';
import { GoFileBinary } from 'react-icons/go';
import { BiLayerPlus, BiLayerMinus, BiShapePolygon, BiCog } from 'react-icons/bi';
import { AiOutlineDownload, AiOutlineUpload } from 'react-icons/ai';
import './style/navbar.css';

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