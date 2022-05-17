import React,{useState, useEffect, useContext} from 'react'



function Notification() {
    
    //로컬에서 불러오기
        function getLocalStorage(key){ return JSON.parse(localStorage[key]); }

    //div 테그 만들기
    function createDiv(key) {
        // 1. <div> element 만들기
        const newDiv_map = document.createElement('img');
        newDiv_map.setAttribute("id", "image_map");
        const newDiv_picture = document.createElement('img');
        newDiv_picture.setAttribute("id", "image_picture");

        const newDiv_name = document.createElement('div');
        var key = 1;
        var obj = JSON.parse(getLocalStorage(key));

        // 2. <div>에 들어갈 text node 만들기
        //이름
        const newname = document.createTextNode(obj.name);
        //지도
        console.log("지도", obj.map);
        console.log("사진", obj.picture);

        document.getElementById("image_map").src = obj.map;
        document.getElementById("image_picture").src = obj.picture;


        // 3. <div>에 text node 붙이기
        newDiv_name.appendChild(newname);

        // 4. <body>에 1에서 만든 <div> element 붙이기
        document.body.appendChild(newDiv_name);
        document.body.appendChild(newDiv_picture);
        document.body.appendChild(newDiv_picture);

      } 
    //   매번 길이를 확인해서, local storage length 를 통해서 계속 제작해준다.


    useEffect( ()=>{ //화면이 열리자 마자 실행이 된다.
        var step
        for (step = 1; step <= localStorage.length; step++){
            //createDIV 가 계속 실행되게 해야 한다.
            createDiv(step);
        }

    }, [])




    return (
        
        <div>
            <p>This is noti page</p>
        </div>
    )
}

export default Notification;