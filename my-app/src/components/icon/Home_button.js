import * as React from "react";

function Home_button(props) {
  return (
    <svg
      width={16}
      height={15}
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      {...props}
    >
      <path
        fillRule="evenodd"
        clipRule="evenodd"
        d="M.707 8.485l1.071-1.07v6.641h12V7.414l1.071 1.071.707-.707-7.07-7.07L7.777 0l-.707.707L0 7.778l.707.707zm2.071 4.571V6.414l5-5 5 5v6.642h-3v-5h-4v5h-3zm4-4v4h2v-4h-2z"
        fill="#fff"
      />
    </svg>
  );
}

export default Home_button;