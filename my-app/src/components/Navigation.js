import React from 'react'
import './navigation.css'
import Plus from './icon/Plus'
import Search from './icon/Search'
import Home_button from './icon/Home_button'
import { Link } from 'react-router-dom';

const Navigation =(props) => {


        return(
            <div className='Navigation'>
                <div className='tabbar'>
                    <div className='plus' onClick={props.onChange} >
                    {/* <Link to ="/walking"><div className='plus_icon'></div></Link> */}
                        <div className='plus_icon'></div>
                        {/* <Plus></Plus> */}
                        {/* SVG로 컴포넌트 만들기보다 이미지로 불러오는게 빠르겠다... */}
                    </div>
                    <div className='search'><Search></Search></div>
                    <div className='home-button'><Home_button></Home_button></div>
                    <div className='bell'></div>
                    <div className='mypage'></div>
                    </div>
		    </div>

        );
    

}

export default Navigation;