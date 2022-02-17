import { FaVectorSquare, FaRegMap } from 'react-icons/fa';
import { GoFileBinary } from 'react-icons/go';
import { BiLayerPlus, BiLayerMinus, BiShapePolygon, BiCog } from 'react-icons/bi';
import { AiOutlineDownload, AiOutlineUpload } from 'react-icons/ai';
import './style/navbar.css';

// https://stackoverflow.com/questions/60877944/react-how-to-pass-an-array-as-props-and-render-a-list-of-images
const Submenu = (props) => {
    const { items } = props;

    /* {items.map(item => {
        <li>item</li>
    })} */
    
    return (
        <>
        <ul className='submenu'>
            <li>Submenu Item</li>
            <li>Submenu Item</li>
            <li>Submenu Item</li>
        </ul>
        </>
    );
};

const Navbar = () => {
    return(
        <>
        <nav>
            <ul>
                <li id='dropdown-icon'>☰</li>
                <li>
                    <BiShapePolygon/>
                    <Submenu items={['Item1', 'Item2']}/>
                </li>
                <li>
                    <GoFileBinary/>
                    <Submenu items={['Item1', 'Item2']}/>
                </li>
                <li>
                    <BiLayerPlus/>
                    <Submenu items={['Item1', 'Item2']}/>
                </li>
                <li>
                    <AiOutlineDownload/>
                    <Submenu items={['Item1', 'Item2']}/>         
                </li>
                <li>
                    <FaRegMap/>
                    <Submenu items={['Item1', 'Item2']}/>
                </li>
                <li>
                    <BiCog/>
                    <Submenu items={['Item1', 'Item2']}/>
                </li>
            </ul>
        </nav>
        </>
    );
};

export default Navbar;