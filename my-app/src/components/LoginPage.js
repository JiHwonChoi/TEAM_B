import React, {useState, useEffect} from 'react'
import './start.css'
import Login from './Login';
import Register from './Register';
import { useNavigate } from "react-router-dom";

function LoginPage(props) {
    let navigate = useNavigate()
    console.log('executed')

    const [article,setArticle] = useState(<Login 
        //여기 보고 로그인 바꾸기
        onSuccess_admin={function(){
            navigate('/admin')
            console.log('success_admin')
    }}   
        onSuccess_user={function(){
        navigate('/start') //admin 여부로 바꿔주기만 하면 될듯
        console.log('success_user')    

    }} onRegister={function(){
        // <Register> 호출하기
        navigate('/Register')

    }}/>)
    return (
        <div className='home-background'>
            {article}
        </div>
    )
}

export default LoginPage;