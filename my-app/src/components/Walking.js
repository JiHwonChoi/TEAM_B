import React, {useState} from 'react'
import Navigation from './Navigation';
import './walking.css';

function Walking () {

        const[left,setLeft] = useState(0)
        const[location, setLocation] = useState('101호')
        const[xclick, setx] = useState(50)
        const[yclick, sety] = useState(50)

        function goleft(){ // 0 327
            let left_margin = left
            left_margin+=327
            if (left_margin>327){
                left_margin = 0
            }

            setLeft(-1 * left_margin)

        } 

        function goright(){
            let left_margin = left
            left_margin+=327
            if(left_margin>327){
                left_margin=327
            }

            setLeft(-1 * left_margin)
            console.log(left)
            
        }

        function imgClick(e){
            console.log(e);
            console.log('click!');
            console.log(e.nativeEvent.offsetX, e.nativeEvent.offsetY);

            setx(e.nativeEvent.offsetX-12)
            sety(e.nativeEvent.offsetY-20)
            // this.setState(
            //     {
            //         clicked:{x:e.nativeEvent.offsetX, y: e.nativeEvent.offsetY},
            //         where:{left:(e.pageX-25) +'px',top: (e.pageY-50) +'px' }
            //     }
            // )
       }
        

        return(
            <div>
			<div className='title'>
                <div className='big_title'>로봇 호출 위치 선택</div>
                <div className='small_title'>현재 위치는 {location} 입니다</div>
            </div>
            <div className='search_tab'>
                    search tab
                </div>

            <div className='slidewrap'>
                <img className='marker' src='marker.png' style={{left:xclick+'px', top:yclick+'px'}}></img>
                <div className='slide' style={{left:left+'px'}} onClick={imgClick}>
                    <img src='mapimg/testmap.jpg'></img>
                    <img src='mapimg/map.png'></img>
                </div>
                
            </div>
            <div className='map_navigate_wrapper'>
                <div className='buttonWrapper' >
                    <div onClick={goleft}> &lt; 이전</div>
                    <div onClick={goright}> 다음 &gt; </div>
                </div>
            </div>
            <div> clicked! x:{xclick} y:{yclick}</div>
            <div className='to_my_location'>산책 시작하기</div>
            <div className='take_stroll'></div>
		    </div>

        );
    }


export default Walking;