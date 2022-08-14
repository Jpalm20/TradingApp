import React, { useState } from 'react'
import { useDispatch } from 'react-redux'
import { register } from '../store/auth'
import { Link } from 'react-router-dom'


export default function Signup() {
  const dispatch = useDispatch();
  const [username, setUsername] = useState();
  const [password, setPassword] = useState();
  const [email, setEmail] = useState();

  const handleSubmit = (e) => {
    e.preventDefault();
    const formName = 'signup';
    dispatch(register({username, email, password, formName}));
  }

  return (
    <div className='container'>
      <h1>Sign Up</h1>
      <p>Email</p>
      <input type='text' autoCapitalize='none' required />
      <p>Username</p>
      <input type='text' autoCapitalize='none' required />
      <p>Password</p>
      <input type='text' autoCapitalize='none' required />
      <button className='submit'>Submit</button>
      <p>Already have an account? <Link to='/login'>Sign in</Link></p>
    </div>
  )
}
