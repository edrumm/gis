import './App.css';
import Layer from './components/layer';
import LayerCollection from './components/layercollection';
import MapWindow from './components/map';
import Navbar from './components/navbar';
import Footer from './components/footer';

function App() {
  return (
    <div className="App">
      <Navbar/>
      <div className='main'>
        <LayerCollection/>
        <MapWindow/>
      </div>
      <Footer/>
    </div>
  );
}

export default App;
