import * as React from "react";
import './icon_style.css'

function Plus(props) {
  return (
    <svg 
      width={14}
      height={14}
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      {...props}
    >
      <path className='plus_icon' d="M14 8H8v6H6V8H0V6h6V0h2v6h6v2z" fill="#000" />
    </svg>
  );
}

export default Plus;