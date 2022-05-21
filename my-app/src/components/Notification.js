import React,{useState, useEffect, useContext} from 'react'
import './Notification.css'




function Notification() {

    const [url,seturl] = useState('')
    
    //div 테그 만들기
    function createDiv(key, data) {
        var obj = data[key].data;
        console.log(obj)
        // 1. <div> element 만들기
        //전체용
        var new_div = document.createElement('div')
        //사진 img 
        var newDiv_picture = document.createElement('img');
        newDiv_picture.id ="image_picture";
        // name 용 div
        var newDiv_name = document.createElement('div');
        var newDiv_location = document.createElement('div');
        //지도로 보여주는 버튼
        var newDiv_button = document.createElement('button');
        // newDiv_button.onclick()

        // 2. <div>에 들어갈 text node 만들기
        //이름
        var location = String(obj.location)
        console.log(typeof(location))
        var newname = document.createTextNode(obj.name);
        var newlocation = document.createTextNode(location);

        console.log(obj.name);
        //지도
        console.log((obj.url))
        //img 테그에 src 지정
        newDiv_picture.src = obj.url;

        // // 3. <div>에 text node 붙이기
        newDiv_name.appendChild(newname);
        newDiv_location.appendChild(newlocation);
        // // 4. <body>에 1에서 만든 <div> element 붙이기
        new_div.appendChild(newDiv_name);
        new_div.appendChild(newDiv_location);
        new_div.appendChild(newDiv_button);
        new_div.appendChild(newDiv_picture);

        var noti = document.getElementById("noti")
        noti.appendChild(new_div)

      } 
    //   매번 길이를 확인해서, local storage length 를 통해서 계속 제작해준다.


      

    useEffect( ()=>{ //화면이 열리자 마자 실행이 된다.
        fetch('http://52.79.237.147:5000/get_image_list')
        .then(res => res.json())
        .then(res => {
            console.log("결과");
            console.log(res);
            var key = res.length
            // console.log(data);
            console.log(res[0]);
            for (var step = 0; step < key; step++){
                createDiv(step, res)
                console.log(step);
            }
        }) 
        
    }, []);
    return (
        <div >
            <p>This is noti page</p>
            <div id='noti'>
                
            </div>
        </div>
    )
}

export default Notification;