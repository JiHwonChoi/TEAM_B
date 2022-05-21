import React from 'react';
import {post} from 'axios';
import axios from 'axios';
import { Link, useNavigate } from "react-router-dom";



axios.defaults.withCredentials = false;
axios.defaults.baseURL = "52.79.237.147:5000";


class Register extends React.Component {


    constructor(props){
        super(props)
        this.state = {
            regi_id : '',
            regi_pw : '',
            regi_pw_check : '',
            regi_name : '',
            regi_code : '',
            regi_number : ''
        }
    }


    register = () => {
        const url = 'http://52.79.237.147:5000/register'
        const formData = new FormData();
        const config = {
            headers : {
                'Access-Control-Allow-Origin': '*',
                'content-type' : 'multipart/form-data'
            }
        }
        formData.append('regi_id', this.state.regi_id);
        formData.append('regi_pw', this.state.regi_pw);
        formData.append('regi_pw_check', this.state.regi_pw_check);
        formData.append('regi_name', this.state.regi_name);
        formData.append('regi_code', this.state.regi_code);
        formData.append('regi_number', this.state.regi_number);
        return post(url, formData, config);
    }

    handleFormSubmit = (event) => {
        console.log(this.props.navigation)
        event.preventDefault();
        this.register().then((res)=> {
            console.log(res)
            if (res.status == 200){
                console.log('hello')
                this.props.navigate('/')
                
                
            }
        })
       
    }

    

    handleValueChange = (event) => {
        let nextState = {};
        nextState[event.target.name] = event.target.value;
        this.setState(nextState);
    }

 

    render () {
        return (
            <div > 
            <form onSubmit={this.handleFormSubmit}>
                <div >
                <h1 id = "domain_register">회원가입 </h1>
                </div>

                <div className='register_grid'>

                <div>
                <label className = "regi">아이디 </label>
                <input type="text" name="regi_id" value={this.state.regi_id} onChange={this.handleValueChange}/>
                </div>

                <div>
                <label className = "regi">패스워드 </label>
                <input type="password" name="regi_pw" value={this.state.regi_pw} onChange={this.handleValueChange}/>
                </div>

                <div>
                <label className = "regi">패스워드 확인 </label>
                <input type="password" name="regi_pw_check" value={this.state.regi_pw_check} onChange={this.handleValueChange}/>
                </div>

                <div>
                <label className = "regi">이름 </label>
                <input type="text" name="regi_name"  value={this.state.regi_name} onChange={this.handleValueChange}/>
                </div>

                <div>
                <label className = "regi">회원코드 </label>
                <input type="text" name="regi_code"  value={this.state.regi_code} onChange={this.handleValueChange}/>
                </div>

                <div>
                <label className = "regi_6">전화번호</label>
                <input type="text" name="regi_number"  value={this.state.regi_number} onChange={this.handleValueChange}/>
                </div>

                <div className='button_regi'>
                <button type="submit">회원가입</button>
                </div>
                </div>
                
            </form>
            <div className='img_register'>

            </div>
            </div>
        )
    }
}


export default Register;
