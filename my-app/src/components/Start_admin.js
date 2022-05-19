import React, {useState, useEffect} from 'react'
import './start.css'
import New from './New';
import Homelogo from './Homelogo';
import Search from './Search';
import HomeAdmin from './Home_admin';
import Notification from './Notification';
import Profile from './Profile';
import Navigation from './Navigation';
import Register from './Register';
import axios from 'axios';
import Login from './Login';
import { socket } from '../service/socket';





function StartAdmin (props) {
        
    const [article, setArticle] = useState(<HomeAdmin />)
    const [title, setTitle] = useState('this is admin app')

    //로컬에 저장
    // function setLocalStorage(key, value){ localStorage.setItem(key,JSON.stringify(value)); }

    //socket 으로 받기
    //1. 사용자 이름이 넘어오기 username
    // 2. 넘어진 사진 넘어오기 picture
    // 3. 지도 넘어오기 map 
    //지도, 사용자 이름, emergency 사진
    // socket.on('emergency', (msg) => {
        // console.log('received')
        //console.log(msg)
       //  var arraymap = new Uint8Array( msg.map );
        // var arraypicture = new Uint8Array( msg.picture );
        // var blob_map = new Blob( [ arraymap ], { type: "image/jpeg" } );
        // var blob_picture = new Blob( [ arraypicture ], { type: "image/jpeg" } );

        // var urlCreator = window.URL || window.webkitURL;
        //담아야 되는 3가지 
        //var imageUrl_map = urlCreator.createObjectURL( blob_map );
        //var imageUrl_picture = urlCreator.createObjectURL( blob_picture );
        // var arrayusername = msg.username ;

        // const alarm_list = {
            //이름 넣기
            // name: arrayusername,
            // map: arraymap,
            // picture: arraypicture,
        // }
        // setLocalStorage(localStorage.length, alarm_list)
    // })
    return(
        <div>
            {console.log('render')}
            <div className='home-background'>
                
                {title}
                <br></br><br></br><br></br>
                {article}
                <Navigation onChange={function(idx){
                    console.log('this is onChange function',idx)
                    if(idx=='plus'){
                        setArticle(<New />)
                    }
                    else if (idx=='search'){
                        setArticle(<Search />)
                    }
                    else if (idx=='home_button'){
                        setArticle(<HomeAdmin />)
                    }
                    else if (idx=='noti'){
                        setArticle(<Notification />)
                    }
                    else if (idx=='profile'){
                        setArticle(<Profile />)
                    }
                    else{
                        setArticle(<HomeAdmin />)
                    }
                    


                } }></Navigation>
            </div>

        
        </div>

    );
    

}

export default StartAdmin;