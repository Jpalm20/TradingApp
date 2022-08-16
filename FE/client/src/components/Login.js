import React, { useState } from 'react'
import { useDispatch } from 'react-redux'
import { authenticate } from '../store/auth'
import '../styles/login.css'


export default function Login() {
  const dispatch = useDispatch();
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    const formName = 'login';
    dispatch(authenticate({username, password, formName}));
  }

  return (
    <div className='container'>
      <h1>Log in</h1>
      <p>Username</p>
      <input type='text' autoCapitalize='none' required />
      <p>Password</p>
      <input type='password' autoCapitalize='none' required />
      <button className='submit'>Submit</button>
    </div>
  )
}
