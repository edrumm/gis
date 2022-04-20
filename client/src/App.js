import React from 'react';
import {BrowserRouter as Router, Route, Routes, Navigate, NavLink} from 'react-router-dom';
import Landing from './pages/landing';
import NotFound from './pages/notFound';
import './App.css';

// https://opensource.com/article/21/3/react-app-hooks
// https://www.techomoro.com/how-to-create-a-multi-page-website-with-react-in-5-minutes/
// https://www.robinwieruch.de/local-storage-react/
// https://pusher.com/tutorials/todo-app-react-hooks/

function App() {
  return (
    <>
      <Router>
        <Routes>
          <Route path="" element={<Landing/>}/>
          <Route path="404" element={<NotFound/>}/>
          {/*<Route path="" element={<Navigate to={Landing}/>}/>*/}
        </Routes>
      </Router>
    </>
  );
}

export default App;
