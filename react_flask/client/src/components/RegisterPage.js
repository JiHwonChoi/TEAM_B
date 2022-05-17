import React, {useState} from 'react'
import Register from './Register';
import { useNavigate } from "react-router-dom";

function RegisterPage() {
    let navigate = useNavigate()
    const [article, setArticle] = useState(<Register navigate={navigate} />)
    return (
        <div>
            {article}
        </div>
    )
}

export default RegisterPage;