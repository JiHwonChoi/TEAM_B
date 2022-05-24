import React, { useState } from 'react';
import {post} from 'axios';
import axios from 'axios';
import{ useEffect } from 'react'
import './Profile.css'
import { useNavigate } from "react-router-dom";
import LoginPage from './LoginPage';



axios.defaults.withCredentials = false;
axios.defaults.baseURL = "localhost:5000";

function Profile() {
    const [name,setName] = useState()
    const [type,setType] = useState()
    let navigate = useNavigate()

    useEffect(()=>{
        //var res;
        //useeffect
        const url = 'http://52.79.237.147:5000/info'
        const config = {
            headers : {
                //'Access-Control-Allow-Origin': '*',
                'content-type' : 'multipart/form-data',
                'Access-Control-Allow-Credentials': true
            }
        }
        const formData = new FormData(); //error
        formData.append("login_status", 'True');
        for(var pair of formData.entries()) {
            console.log(pair[0]+ ', '+ pair[1]);
        }
        post(url, formData, config).then((res)=> {
            console.log(res)
            console.log('아이디' + res.data.Data);
            setName(res.data.Data)
            // console.log(name)
            console.log('사용자 타입' + res.data.Type);
            console.log(typeof res.data.Type)
            if (res.data.Type == true){
                setType('관리자')
            } 
            else{
                setType('사용자')
            }
            console.log(type)
        })
    });

    return ( //안에는 html 짜기
        <div className='grid'>
            {/* 먼저 전체 DIV를 쪼개자 */}
            <div className='grid_1'>
                {/* 하늘색으로 채우기*/}
            </div>

            <div className='grid_2'>
                <div className = "grid_2_1">
                <div className='name'>{name}</div>
                {/* 김준서 */}
                <div className='type'>{type}</div>
                </div>
                <div className='grid_2_button_1'>
                {/*두번째 버튼*/}
                프로필 수정
                </div>
            </div>

            <div className='grid_3'>
                {/*라우터가 다른 곳이면 navigate*/}
                {/*컴포넌트 교체를 위해서는 prop를 통해서 state 교체*/}

                <div className='grid_3_1' onClick={function(){
                    navigate('/')

                }}>
                {/*로그아웃*/}
                로그아웃
                </div>

                <div className='grid_3_2' onClick={() => window.open('http://pf.kakao.com/_pCxeLb/chat', '_blank')}>

                {/*1대 1 문의 -> 카카오톡 오픈 채팅방 개설*/}
                1대1 문의
                </div>


            </div>
        </div>
    )
}

export default Profile;