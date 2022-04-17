import React, {useState} from 'react'
import { Link } from 'react-router-dom';
import './start.css'
import New from './New';
import Homelogo from './Homelogo';
import Search from './Search';
import Home from './Home';
import Notification from './Notification';
import Profile from './Profile';
import Navigation from './Navigation';


function Start (props) {
        
        const [article, setArticle] = useState(<Homelogo />)

        return(
            <div>
                {console.log('render')}
                <div className='home-background'>
                    {/* <div className='sebotage_1'></div>
                    <div className='logo'></div> */}
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
                            setArticle(<Home />)
                        }
                        else if (idx=='noti'){
                            setArticle(<Notification />)
                        }
                        else if (idx=='profile'){
                            setArticle(<Profile />)
                        }
                        else{
                            setArticle(<Homelogo />)
                        }
                        
                    } }></Navigation>
                </div>
                {/* <Link to ="/main">메인페이지</Link>
                <br></br>
                <Link to ="/page1">page1</Link> */}
			
		    </div>

        );
    

}

export default Start;