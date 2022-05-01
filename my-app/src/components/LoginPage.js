import React, {useState, useEffect} from 'react'
import './start.css'
import Login from './Login';
import Register from './Register';
import { useNavigate } from "react-router-dom";

function LoginPage(props) {
    let navigate = useNavigate()
    console.log('executed')

    const [article,setArticle] = useState(<Login 
        onSuccess={function(){
       navigate('/start')
        console.log('success')
    }} onRegister={function(){
        // <Register> 호출하기
        navigate('/Register ')
    }}/>)
    return (
        <div className='loginPage'>
            {article}
        </div>
    )
}

export default LoginPage;