import React, { useState } from 'react'
import { useDispatch } from 'react-redux'
import { register } from '../store/auth'
import { Link } from 'react-router-dom'


export default function Signup() {
  const dispatch = useDispatch();
  const [first_name, setFirstName] = useState();
  const [last_name, setLastName] = useState();
  const [birthday, setBirthday] = useState();
  const [email, setEmail] = useState();
  const [password, setPassword] = useState();
  const [street_address, setStreetAddress] = useState();
  const [city, setCity] = useState();
  const [state, setState] = useState();
  const [country, setCountry] = useState();

  const handleSubmit = (e) => {
    e.preventDefault();
    const formName = 'signup';
    dispatch(register({first_name,last_name,birthday,email,password,street_address,city,state,country}));
  }

  return (
    <div className='container'>
      <h1>Sign Up</h1>
      <p>First Name</p>
      <input type='text' autoCapitalize='none' required onChange={(e)=>setFirstName(e.target.value)}/>
      <p>Last Name</p>
      <input type='text' autoCapitalize='none' required onChange={(e)=>setLastName(e.target.value)}/>
      <p>Birthday</p>
      <input type='text' autoCapitalize='none' required onChange={(e)=>setBirthday(e.target.value)}/>
      <p>Email</p>
      <input type='text' autoCapitalize='none' required onChange={(e)=>setEmail(e.target.value)}/>
      <p>Password</p>
      <input type='text' autoCapitalize='none' required onChange={(e)=>setPassword(e.target.value)}/>
      <p>Street Address</p>
      <input type='text' autoCapitalize='none' required onChange={(e)=>setStreetAddress(e.target.value)}/>
      <p>City</p>
      <input type='text' autoCapitalize='none' required onChange={(e)=>setCity(e.target.value)}/>
      <p>State</p>
      <input type='text' autoCapitalize='none' required onChange={(e)=>setState(e.target.value)}/>
      <p>Country</p>
      <input type='text' autoCapitalize='none' required onChange={(e)=>setCountry(e.target.value)}/>
      <button className='submit' onClick={handleSubmit}>Submit</button>
      <p>Already have an account? <Link to='/login'>Sign in</Link></p>
    </div>
  )
}
