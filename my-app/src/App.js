import logo from './logo.svg';
import './App.css';
import './components/Header'
import Header from './components/Header'
import Main from './components/Main'
import Page1 from './components/Page1'
import NotFound from './components/NotFound';
import Home from './components/Home';
import React from "react";
import Walking from './components/Walking';
import { BrowserRouter, Route, Routes } from 'react-router-dom';

const App =() => {
  return (
    <div className="App">


      <BrowserRouter>
        <Header />
        <Routes>
        <Route path="/" element={<Home/>}></Route>
          <Route path="/main" element={<Main />}></Route>
          <Route path="*" element={<NotFound />}></Route>
          <Route path="/Page1" element={<Page1></Page1>}></Route>
          <Route path="/walking" element={<Walking></Walking>}></Route>
        </Routes>

      </BrowserRouter>
      
    </div>
  )
}

export default App;