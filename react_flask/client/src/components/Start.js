import React, {useState, useEffect} from 'react'
import './start.css'
import New from './New';
import Homelogo from './Homelogo';
import Search from './Search';
import Home from './Home';
import Notification from './Notification';
import Profile from './Profile';
import Navigation from './Navigation';
import Register from './Register';
import axios from 'axios';
import Login from './Login';






function Start (props) {
        
        const [article, setArticle] = useState(<Homelogo />)
        const [title, setTitle] = useState('empty')

        //api 지속적으로 새로고침 하는 함수
        // function getapi (i){
        //     let timer = setInterval(async ()=>{
        //         i=i+1
        //         let my_url='https://jsonplaceholder.typicode.com/todos/'+i
        //         let response = await axios.get(my_url)
        //         console.log(response.data)
        //         let title = response.data.title
        //         setTitle(title)
        //         if(i>10){
        //             clearTimeout(timer)
        //             console.log('clear')
        //         }
        //         //받아온 정보로 state를 지속적으로 업데이트 하기
        
        //     },200)    
        // }


        // 렌더링이 처음 됐을때 한번 받아오기
        // useEffect 를 react 에서 임포트 해와야함
        // useEffect(async ()=>{
            
        //     let my_url = 'https://jsonplaceholder.typicode.com/todos/1'
        //     let response = await axios.get(my_url)
        //     console.log(response.data)
        // },[])

        return(
            <div>
                {console.log('render')}
                <div className='home-background'>
                    
                    {article}
                    <br></br><br></br><br></br>
                    {title}
                    <Navigation onChange={function(idx){
                        console.log('this is onChange function',idx)
                        if(idx=='plus'){
                            setArticle(<New />)
                        }
                        else if (idx=='search'){
                            setArticle(<Search />)
                        }
                        else if (idx=='home_button'){
                            setArticle(<Home />)
                        }
                        else if (idx=='noti'){
                            setArticle(<Notification />)
                        }
                        else if (idx=='profile'){
                            setArticle(<Profile />)
                        }
                        else{
                            setArticle(<Home />)
                        }
                        


                    } }></Navigation>
                </div>

			
		    </div>

        );
    

}

export default Start;