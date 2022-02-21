import './App.css';
import Layer from './components/layer';
import LayerCollection from './components/layercollection';
import MapWindow from './components/map';
import Navbar from './components/navbar';

function App() {
  return (
    <div className="App">
      <Navbar/>
      <div className='main'>
        <LayerCollection/>
        <MapWindow/>
      </div>
    </div>
  );
}

export default App;
