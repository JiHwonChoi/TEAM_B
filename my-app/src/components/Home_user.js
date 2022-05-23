import React from 'react'
import './Home.css'

function HomeUser(props) {
    return (
        <div className='home'>
            <div className='sebotage_logo'></div>
            <div className='btn walking' 
            onClick={()=>{props.callWalkPage()}}>
                산책하기</div>

            <div className='btn walking'>
                내 정보 확인하기</div>

            <div className='btn walking' >
                위급 알림 보내기</div>
        </div>
    )
}

export default HomeUser;