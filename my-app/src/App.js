import logo from './logo.svg';
import './App.css';
import Main from './components/Main'
import Page1 from './components/Page1'
import NotFound from './components/NotFound';
import Start from './components/Start';
import LoginPage from './components/LoginPage';
import RegisterPage from './components/RegisterPage';
import React from "react";
import Walking from './components/Walking';
import { BrowserRouter, Route, Routes } from 'react-router-dom';

const App =() => {
  return (
    <div className="App">


      <BrowserRouter>
    
        <Routes>
          {/* <Route path="/" element={<LoginPage />}></Route> */}
          <Route path="/" element={<Start />}></Route>
          <Route path="/register" element={<RegisterPage />}></Route>
          <Route path="*" element={<NotFound />}></Route>
          <Route path="/Page1" element={<Page1></Page1>}></Route>
          <Route path="/walking" element={<Walking></Walking>}></Route>
          <Route path="/start" element={<Start />}></Route>
        </Routes>

      </BrowserRouter>
      
    </div>
  )
}

export default App;
