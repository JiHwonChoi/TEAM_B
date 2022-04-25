import React from 'react'
import './new.css'

function New() {
    return (
        <div>
            <div className='title'>
                <div className='big_title'>로봇 역할 카테고리</div>
                <div className='small_title'>원하시는 카테고리를 선택해주세요</div>
            </div>
            <div className='search_tab'>
                    search tab
                </div>

            <div className='robot_current'>
                display robot location
            </div>
            <div className='detail'>goto detail page</div>
            <div className='to_my_location'>goto mylocation page</div>
            <div className='take_stroll'></div>

        </div>
    )
}

export default New;