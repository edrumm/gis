import './App.css';
import Layer from './components/layer';
import LayerCollection from './components/layercollection';
import MapWindow from './components/map';
import Navbar from './components/navbar';
import Footer from './components/footer';
import Upload from './components/upload';

/*function App() {
  return (
    <div className="App">
      <Navbar/>
      <div className='main'>
        <LayerCollection/>
        <MapWindow/>
      </div>
      <Upload/>
      <Footer/>
    </div>
  );
}*/

function App() {
  return (
    <div className="App"> 
      <Upload/>
    </div>
  );
}

export default App;
