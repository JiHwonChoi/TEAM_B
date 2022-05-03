
import React from 'react';
import {post} from 'axios';
import axios from 'axios';


axios.defaults.withCredentials = false;
axios.defaults.baseURL = "localhost:5000";

function Profile() {
    var ID;
    var res;
    //useeffect
    window.addEventListener('DOMContentLoaded', function()
    {
        const url = 'http://127.0.0.1:5000/info'
        const formData = new FormData();
        const config = {
            headers : {
                'Access-Control-Allow-Origin': '*',
                'content-type' : 'multipart/form-data'
            }
        }
        formData.append("login_status", "True");
        post(url, formData, config);

        //console을 통해서 값을 가져와서 변수에 담기
        console.log(post(url, formData, config));
        res = console.log(post(url, formData, config));
        if (res.status === 200){
            ID = res.Id;
        }

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