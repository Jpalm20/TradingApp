import React, { useState } from 'react'
import { useDispatch } from 'react-redux'
import { authenticate } from '../store/auth'
import '../styles/login.css'


export default function Login() {
  const dispatch = useDispatch();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    const formName = 'login';
    dispatch(authenticate({email, password, formName}));
  }

  return (
    <div className='container'>
      <h1>Log in</h1>
      <p>Email</p>
      <input type='text' autoCapitalize='none' required onChange={(e)=>setEmail(e.target.value)}/>
      <p>Password</p>
      <input type='password' autoCapitalize='none' required onChange={(e)=>setPassword(e.target.value)}/>
      <button className='submit' onClick={handleSubmit}>Submit</button>
    </div>
  )
}
