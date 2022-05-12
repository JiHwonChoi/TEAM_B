import React, {Component} from 'react'
import Navigation from './Navigation';

class Walking extends Component {

    render(){

        return(
            <div>
			<div className='title'>
                <div className='big_title'>로봇 역할 카테고리</div>
                <div className='small_title'>산책로를 선택해주세요</div>
            </div>
            <div className='search_tab'>
                    search tab
                </div>

            <div className='robot_current'>
                지도 이미지 표시
            </div>
            <div className='detail' >지도 선택하기</div>
            <div className='to_my_location'>산책 시작하기</div>
            <div className='take_stroll'></div>
		    </div>

        );
    }

}

export default Walking;