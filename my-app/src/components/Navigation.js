import React from 'react'
import './navigation.css'
import { Link } from 'react-router-dom';

const Navigation =(props) => {


        return(
            <div className='Navigation'>
                <div className='tabbar'>
                    <div className='plus' onClick={()=> props.onChange('plus')} >
                        <div className='plus_icon'></div>  
                    </div>
                    {/* <div className='search' onClick={()=> props.onChange('search')}>
                        <div className='search_icon'></div>
                    </div> */}
                    <div className='home-button' onClick={()=> props.onChange('home_button')}>
                        <div className='home_icon'></div>
                    </div>
                    <div className='noti' onClick={()=> props.onChange('noti')}>
                        <div className='noti_icon'></div>
                    </div>
                    <div className='profile' onClick={()=> props.onChange('profile')}>
                        <div className='profile_icon'></div>
                    </div>
                    </div>
		    </div>

        );
    

}

export default Navigation;