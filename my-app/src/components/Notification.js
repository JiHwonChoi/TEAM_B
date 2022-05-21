import React,{useState, useEffect, useContext} from 'react'



function Notification() {

    const [url,seturl] = useState('')
    
    //div 테그 만들기
    function createDiv(key, data) {
        var obj = data[key];
        // 1. <div> element 만들기
        const newDiv_picture = document.createElement('img');
        newDiv_picture.setAttribute("id", "image_picture");

        const newDiv_name = document.createElement('div');

        // 2. <div>에 들어갈 text node 만들기
        //이름
        const newname = document.createTextNode(obj.name);
        //지도
        document.getElementById("image_map").src = obj.map;
        document.getElementById("image_picture").src = obj.picture;


        // // 3. <div>에 text node 붙이기
        newDiv_name.appendChild(newname);

        // // 4. <body>에 1에서 만든 <div> element 붙이기
        document.body.appendChild(newDiv_name);
        document.body.appendChild(newDiv_picture);
      } 
    //   매번 길이를 확인해서, local storage length 를 통해서 계속 제작해준다.


    useEffect( ()=>{ //화면이 열리자 마자 실행이 된다.
        fetch('http://52.79.237.147:5000/get_image_list')
        .then(res => {
            console.log("결과");
            var data = res.json();
            console.log(data);
            var key = data.length;
            console.log(data);
            for (var step = 0; step < key; step++){
                createDiv(step, data)
            }
        }) 
        
    }, []);




    return (
        
        <div>
            <p>This is noti page</p>
            <img src={url}></img>
        </div>
    )
}

export default Notification;