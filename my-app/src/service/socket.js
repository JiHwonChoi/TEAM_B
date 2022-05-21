import { createContext } from "react";
import socketIo from "socket.io-client";

// export const socket = socketIo(String('http://127.0.0.1:5000'), { withCredentials: true });
export const socket = socketIo(String('http://52.79.237.147:5000:5000'), { withCredentials: true });
export const SocketContext = createContext(socket);

socket.on("connect", () => {
  console.log("socket server connected.");
});

socket.on("disconnect", () => {
  console.log("socket server disconnected.");
});