import React, { useState } from 'react';
import {post} from 'axios';
import axios from 'axios';
import{ useEffect } from 'react'
axios.defaults.withCredentials = false;
axios.defaults.baseURL = "localhost:5000";

function Profile() {
    var ID;

    useEffect(()=>{
        //var res;
        //useeffect
        const url = 'http://127.0.0.1:5000/info'
        const config = {
            headers : {
                'Access-Control-Allow-Origin': '*',
                'content-type' : 'multipart/form-data'
            }
        }
        const formData = new FormData(); //error
        formData.append("login_status", 'True');
        for(var pair of formData.entries()) {
            console.log(pair[0]+ ', '+ pair[1]);
        }
        post(url, formData, config).then((res)=> {
            console.log(res);
        })

        
        //console.log(post(url, formData, config));
        //res = console.log(post(url, formData, config));
        //if (res.status === 200){
        //    ID = res.Id;
        //}
    });
    
    return ( //안에는 html 짜기
        <div>
            <p>This is profile page</p>
            <div> 
                회원명:{ID}
            </div>
        </div>
    )
}

export default Profile;