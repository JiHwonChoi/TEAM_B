import React, {Component} from 'react'
import { Link } from 'react-router-dom';
import './home.css'

import Navigation from './Navigation';

function Home (props) {
        let i = 0

        function hello(){
            let _article
            if (i==0){
                _article='i=0'
                i=1
            }
            else {
                _article='i=1'
                i=0
            }
            return _article
        }
        return(
            <div>
                <div className='home-background'>
                    <div className='sebotage_1'></div>
                    <div className='logo'></div>
                    {hello()}
                    <Navigation onChange={function(){
                        console.log('this is onChange function',i)
                        if(i==0){
                            i=1
                        }
                        else {i=0}
                        
                    } }></Navigation>
                </div>
                {/* <Link to ="/main">메인페이지</Link>
                <br></br>
                <Link to ="/page1">page1</Link> */}
			
		    </div>

        );
    

}

export default Home;