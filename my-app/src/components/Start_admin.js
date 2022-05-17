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





function StartAdmin (props) {
        
        const [article, setArticle] = useState(<HomeAdmin />)
        const [title, setTitle] = useState('this is admin app')

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