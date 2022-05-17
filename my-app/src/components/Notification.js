import React from 'react'

function createDiv() {
    // 1. <div> element 만들기
    const newDiv = document.createElement('div');
    
    // 2. <div>에 들어갈 text node 만들기
    const newText = document.createTextNode('안녕하세요');
    
    // 3. <div>에 text node 붙이기
    newDiv.appendChild(newText);
    
    // 4. <body>에 1에서 만든 <div> element 붙이기
    document.body.appendChild(newDiv);
  } 

function Notification() {

    return (
        
        <div>
            <p>This is noti page</p>
        </div>
    )
}

export default Notification;