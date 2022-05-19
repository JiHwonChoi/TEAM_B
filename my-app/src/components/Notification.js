import React,{useState, useEffect, useContext} from 'react'



function Notification() {

    const [url,seturl] = useState('')
    
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
        var key = 1; //제거 필요
        // var obj = JSON.parse(getLocalStorage(key));
        var obj = getLocalStorage(key);
        console.log(obj)

        var blob_map = new Blob( [ obj.map ], { type: "image/jpeg" } );
        var blob_picture = new Blob( [ obj.picture ], { type: "image/jpeg" } )
        var urlCreator = window.URL || window.webkitURL;
        //담아야 되는 3가지 
        var imageUrl_map = urlCreator.createObjectURL(blob_map);
        var imageUrl_picture = urlCreator.createObjectURL(blob_picture);
        console.log(imageUrl_map)
        console.log(typeof(imageUrl_map))
        seturl(imageUrl_map)

        // 2. <div>에 들어갈 text node 만들기
        //이름
        // const newname = document.createTextNode(obj.name);
        //지도
        // document.getElementById("image_map").src = obj.map;
        // document.getElementById("image_picture").src = obj.picture;


        // // 3. <div>에 text node 붙이기
        // newDiv_name.appendChild(newname);

        // // 4. <body>에 1에서 만든 <div> element 붙이기
        // document.body.appendChild(newDiv_name);
        // document.body.appendChild(newDiv_picture);
        // document.body.appendChild(newDiv_picture);

      } 
    //   매번 길이를 확인해서, local storage length 를 통해서 계속 제작해준다.


    useEffect( ()=>{ //화면이 열리자 마자 실행이 된다.
        var step;
        var length = localStorage.length;
        for (step = 0; step < length; step++){
            //createDIV 가 계속 실행되게 해야 한다.
            console.log("here")
            createDiv(step);
        }

    }, [])




    return (
        
        <div>
            <p>This is noti page</p>
            <img src={url}></img>
        </div>
    )
}

export default Notification;