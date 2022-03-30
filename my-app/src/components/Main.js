import React from 'react'
import { Link } from 'react-router-dom';

const Main = (props) => {
    //     constructor (props){
    //         super(props);
    //         this.imgClick=this.imgClick.bind(this);
    //     }

    //    imgClick(e){
    //         console.log('click!');
    //    }

   
        return(
            <div>
			<h1>main page</h1>
            <h3>Current location</h3>
            <img src='mapimg/map.png'></img>
            <Link to ="/Page1">
                <h3>Page1</h3>
            </Link>
		    </div>

        );
    

}

export default Main;