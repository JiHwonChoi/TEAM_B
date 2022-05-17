import React from 'react'
import styles from './div_border.module.css'
import './Home.css'


function HomeAdmin() {
    return (
        <div className='home'>
            <div className='sebotage_logo'></div>
            <div className='btn walking'>오늘 로그 확인하기</div>
            <div className='btn walking'>경고 로그 확인하기</div>
            <div className='btn walking'>충전소로 로봇 이동</div>
        </div>
    )
}

export default HomeAdmin;