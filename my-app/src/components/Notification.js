import React,{useState, useEffect, useContext} from 'react'
import './Notification.css'
import {post} from 'axios';
import axios from 'axios';

import jquery from 'jquery'
import $ from 'jquery'
import swing from 'jquery'



var num = '0';
var imgUrl = [];

function Notification() {
    

    axios.defaults.withCredentials = false;
    axios.defaults.baseURL = "52.79.237.147:5000";

    // const [url,seturl] = useState('')
    // const [array, setarray] = useState()
    // const [map, setmap] = useState()
     const [im, setim] = useState('')
    //const [imgurl, setimgurl] = useState()
    const [number, setNumber] = useState()

    function onbutton(key){
        //var box_review = document.getElementsByClassName("review_"+key);
        //var box_main = document.getElementsByClassName("main_"+key);
        //box_review.style.display = "block";
        //box_main.style.display = "none";
        $(".review_"+key).toggle(500,swing)
        $(".main_"+key).toggle(500,swing)
    }

    //div 테그 만들기
    function createDiv(key, data) {
        var obj = data[key].data;

        // 1. <div> element 만들기
        //전체용
        var new_div = document.createElement('div')
        new_div.id = 'main';
        new_div.className = 'main_'+key;
        var new_div_review = document.createElement('div')
        new_div_review.id = "review";
        new_div_review.className = "review_"+key;
        var new_line= document.createElement('hr')
        new_line.id = "line";

        //사진 img 
        var newDiv_picture = document.createElement('img');
        newDiv_picture.id ="image_picture_"+key;
        // name 용 div
        var newDiv_name = document.createElement('div');
        var newDiv_location = document.createElement('div');
        //지도로 보여주는 버튼
        var newDiv_button = document.createElement('button');
        newDiv_button.innerHTML = "지도 보기"
        newDiv_button.id = 'button_DIV'
        //함수 넣기
        newDiv_button.onclick=() => {
            if (num == '0'){
                notification_post(key)
                console.log("김준서 test:" + imgUrl)
            }
            else if (num == '1'){
                original_picture(key)
            }
            }

        var css_button = document.createElement('button');
        css_button.innerHTML = "상세보기"
        css_button.id = 'button_css'
        css_button.onclick=() => onbutton(key)

        var css_button_1 = document.createElement('button');
        css_button_1.innerHTML = "요약하기"
        css_button_1.id = 'button_css'
        css_button_1.onclick=() => onbutton(key)



        // 2. <div>에 들어갈 text node 만들기
        //이름
        var location = String(obj.location)
        var alarm = document.createTextNode("Emergency is occured by "+obj.name)
        var newname = document.createTextNode("User name: "+ obj.name);
        var newlocation = document.createTextNode("발생 장소: " + location);

        //지도
        //img 테그에 src 지정
        newDiv_picture.src = obj.url;
        imgUrl.push(obj.url);
        console.log(obj.url);
        console.log(imgUrl);

        //setim(newDiv_picture);

        // // 3. <div>에 text node 붙이기
        newDiv_name.appendChild(newname);
        newDiv_location.appendChild(newlocation);
        newDiv_location.id = "location_"+key;
        // // 4. <body>에 1에서 만든 <div> element 붙이기
        new_div.appendChild(newDiv_name);
        new_div.appendChild(newDiv_location);
        new_div.appendChild(newDiv_button);
        new_div.appendChild(newDiv_picture);
        new_div.appendChild(css_button_1);

        //요약 본에 넣기
        new_div_review.appendChild(alarm);
        new_div_review.appendChild(css_button);
        //new_div_review.appendChild(newDiv_name);


        var noti = document.getElementById("noti")
        noti.appendChild(new_div_review)
        //noti.appendChild(new_line)
        noti.appendChild(new_div)

      } 
    //   매번 길이를 확인해서, local storage length 를 통해서 계속 제작해준다.

    function notification_post(key){
        const url = 'http://52.79.237.147:5000/get_map'
        const config = {
            headers : {
                // 'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Credentials': true,
                'content-type' : 'multipart/form-data'
            }
        }
        var loc = document.getElementById("location_"+key).innerHTML.split(" ")[2]
        var data_location = {"location": loc}
        var json_location = JSON.stringify(data_location)
        console.log(json_location)
        post(url, json_location, config).then((res) => { //에러 발생
            console.log(number)
            get_map(key, res);

        })
    }

    // 사진 넣기가 안됨
    function get_map(key, data){
        var img_blob = data.data.map;
        const byteCharacters = atob(img_blob);
        const byteNumbers = new Array(byteCharacters.length);
        for (let i = 0; i < byteCharacters.length; i++) {
            byteNumbers[i] = byteCharacters.charCodeAt(i);
        }
        var arrayBufferView = new Uint8Array( byteNumbers  );
        var blob = new Blob( [ arrayBufferView ], { type: "image/jpeg" } );
        var urlCreator = window.URL || window.webkitURL;
        var imageUrl = urlCreator.createObjectURL( blob );
        //setimgurl(imageUrl)
        var image_map = document.getElementById("image_picture_"+key)
        image_map.src = imageUrl;
        num = "1";
        console.log(number)
    }

    function original_picture(key){
        get_origin(key);
    }

    function get_origin(key){
        var image_map = document.getElementById("image_picture_"+key)
        image_map.src = imgUrl[key];
        console.log("여기용1 "+ num)
        num = "0";
        console.log("여기용2 "+ num)

    }

    useEffect( ()=>{ //화면이 열리자 마자 실행이 된다.
        fetch('http://52.79.237.147:5000/get_image_list')
        .then(res => res.json())
        .then(res => {
            var key = res.length
            for (var step = 0; step < key; step++){
                createDiv(step, res)
            }
            console.log("useeffect");
        }) 
    }, []);

    return (
        <div >
            <div id = "domain"></div>
            <div id = "title">Emergency Alarm</div>
            <div id='noti'>
            {/* <img src= {im}></img> */}
            </div>
            
        </div>
    )
}

export default Notification;