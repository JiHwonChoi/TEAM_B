import logo from './logo.svg';
import './App.css';
import Main from './components/Main'
import Page1 from './components/Page1'
import NotFound from './components/NotFound';
import Start from './components/Start';
import LoginPage from './components/LoginPage';
import RegisterPage from './components/RegisterPage';
import React , {useEffect} from "react";
import StartAdmin from './components/Start_admin';
import Walking from './components/Walking';
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import { socket, SocketContext } from "./service/socket";

const useNotification = (title, options) => {
  if (!("Notification" in window)) {
    return;
  }
  const fireNotif = () => {
    /* 권한 요청 부분 */
    if (Notification.permission !== "granted") {
      Notification.requestPermission().then((permission) => {
        if (permission === "granted") {
          /* 권한을 요청받고 nofi를 생성해주는 부분 */
          new Notification(title, options);
          console.log('1')
        } 
        else {
          console.log("2")
          return;
        }
      });
    } 
    else {
      console.log("3")
      /* 권한이 있을때 바로 noti 생성해주는 부분 */
      new Notification(title, options);
    }
  };
  console.log("4")
  return fireNotif();
};

const App =() => {
  useEffect(() => {
    return () => {
      socket.disconnect();
    }
  }, []);

  

  socket.on('state', (msg) => {
    // console.log('received')
    console.log('received')
    //요기에다가 추가하면 됨
    useNotification("Emergency alert", {
      body: "emergency is occured" });
    console.log("ok")
})


  return (

    <SocketContext.Provider value={socket}>
    <div className="App">


      <BrowserRouter>
        <Routes>
          <Route path="/" element={<LoginPage />}></Route>
          {/* <Route path="/" element={<Start />}></Route> */}
          <Route path="/register" element={<RegisterPage />}></Route>
          <Route path="*" element={<NotFound />}></Route>
          <Route path="/Page1" element={<Page1></Page1>}></Route>
          <Route path="/walking" element={<Walking></Walking>}></Route>
          <Route path="/start" element={<Start />}></Route>
          <Route path="/admin" element={<StartAdmin />}></Route>
        </Routes>

      </BrowserRouter>
      
    </div>
    </SocketContext.Provider>
  )
}

export default App;
