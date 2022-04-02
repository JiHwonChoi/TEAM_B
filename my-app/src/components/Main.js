import React, { Component } from 'react'
import { Link } from 'react-router-dom';

class Main extends Component {
        constructor (props){
            super(props);
            this.state={
                marker:'marker.png',
                clicked:{x:0, y:0},
                    
                where:{
                    top: '50%', left: '50%'
                }
            }

    
        }

    

       imgClick(e){
            console.log(e);
            console.log('click!');
            console.log(e.nativeEvent.offsetX, e.nativeEvent.offsetY);
            this.setState(
                {
                    clicked:{x:e.nativeEvent.offsetX, y: e.nativeEvent.offsetY},
                    where:{left:(e.pageX-25) +'px',top: (e.pageY-50) +'px' }
                }
            )
       }

       render(){



        return(
            <div>
			<h1>main page</h1>
            <h3>Current location</h3>
            <img src='mapimg/map.png' onClick={this.imgClick.bind(this)}></img>
            <img className='marker' src={this.state.marker} alt='hello' style={this.state.where}></img>
            <h3>This is where clicked on image : {this.state.clicked.x} , {this.state.clicked.y}</h3>
            <h3>This is where markers at: {this.state.where.top}, {this.state.where.left}</h3>
            <Link to ="/Page1">
                <h3>Page1</h3>
            </Link>
		    </div>

        );

       }
    

}

export default Main;