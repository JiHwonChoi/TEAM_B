import React, {Component} from 'react'
import { Link } from 'react-router-dom';
import './home.css'
import Plus from './icon/Plus'
import Search from './icon/Search'
import Home_button from './icon/Home_button'

function Home (props) {



        return(
            <div>
                <div className='home-background'>
                    <div className='sebotage_1'></div>
                    <div className='logo'></div>
                    <div className='tabbar'>
                        <div className='plus'>
                            {/* <div className='img_plus'></div> */}
                            <Plus></Plus>
                            {/* SVG로 컴포넌트 만들기보다 이미지로 불러오는게 빠르겠다... */}
                        </div>
                        <div className='search'><Search></Search></div>
                        <div className='home-button'><Home_button></Home_button></div>
                        <div className='bell'></div>
                        <div className='mypage'></div>
                    </div>
                </div>
                {/* <Link to ="/main">메인페이지</Link>
                <br></br>
                <Link to ="/page1">page1</Link> */}
			
		    </div>

        );
    

}

export default Home;