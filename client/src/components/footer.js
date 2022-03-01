import './style/footer.css';
import { FaGithub } from 'react-icons/fa';
import { VscMortarBoard } from 'react-icons/vsc';

const Footer = () => {

    return (
        <>
        <div className='footer-container'>
            <footer>
                &copy; Ewan Drummond 2022<br/>
                <a href='https://github.com/edrumm/gis' title='GitHub repository' target='_blank'>
                    <FaGithub/>
                </a>
                <a href='https://hw.ac.uk' title='Heriot-Watt University' target='_blank'>
                    <VscMortarBoard/> 
                </a>
            </footer>
        </div>
        </>
    );

};

export default Footer;