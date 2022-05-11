import logo from './logo.svg';
import './App.css';
import Main from './components/Main'
import Page1 from './components/Page1'
import NotFound from './components/NotFound';
import Start from './components/Start';
import LoginPage from './components/LoginPage';
import RegisterPage from './components/RegisterPage';
import React , {useEffect} from "react";
import Walking from './components/Walking';
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import { socket, SocketContext } from "./service/socket";

const App =() => {
  useEffect(() => {
    return () => {
      socket.disconnect();
    }
  }, []);

  socket.on('state', (msg) => {
    console.log('received')
    //요기에다가 추가하면 됨
    
})


  return (

    <SocketContext.Provider value={socket}>
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
    </SocketContext.Provider>
  )
}

export default App;
