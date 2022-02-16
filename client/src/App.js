import './App.css';
import Layer from './components/layer';
import LayerCollection from './components/layercollection';
import Map from './components/map';
import Navbar from './components/navbar';

function App() {
  return (
    <div className="App">
      <Navbar/>
      <div className='main'>
        <LayerCollection/>
        <Map/>
      </div>
    </div>
  );
}

export default App;
