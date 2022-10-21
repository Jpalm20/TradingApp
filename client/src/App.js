import React, { useEffect, Fragment, useState } from "react";
import { useSelector, useDispatch } from "react-redux";
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Navigate,
  Redirect
} from "react-router-dom";
import { me, getTrades } from "./store/auth";
import Home from "./components/Home";
import Login from "./components/Login";
import Signup from "./components/Signup";
import LogTrade from "./components/LogTrade";
import Navbar from "./components/Navbar";
import UserProfile from "./components/UserProfile";
import Summary from "./components/Summary";

export default function App() {
  const dispatch = useDispatch();
  const { user } = useSelector((state) => state.auth);
  const { trades } = useSelector((state) => state.auth);
  const isLoggedIn = ((user && Object.keys(user).length > 2) ? (true):(false));
  const hasTrades = ((trades && trades.trades && Object.keys(trades.trades).length > 0) ? (true):(false));
  const noTrades = ((trades && trades.trades && Object.keys(trades.trades).length === 0) ? (true):(false));

  
  useEffect(() => {
    async function getUserTrades(){
      if(isLoggedIn && !hasTrades && !noTrades){
        const user_id = user.user_id;
        await dispatch(getTrades({ user_id }));
      }
    }
    getUserTrades();
  })
  
  
  return (
    <Fragment>
      <Router>
        <Navbar user={user} />
        <Routes>
          {isLoggedIn ? (
            <>
              <Route path="/" element={<Home user={user}/>} />
              <Route path="/login" element={<Navigate to="/profile"/>} />
              <Route path="/signup" element={<Navigate to="/"/>} />
              <Route path="/logTrade" element={<LogTrade user={user}/>} />
              <Route path='/profile' element={<UserProfile user={user}/>} />
              <Route path='/summary' element={<Summary user={user}/>} />
            </>
          ) : (
            <>
              <Route path="/" element={<Navigate to="/login" />} />
              <Route path="/profile" element={<Navigate to="/login"/>} />
              <Route path="/logTrade" element={<Navigate to="/login"/>} />
              <Route path='/summary' element={<Navigate to="/login"/>} />
              <Route path="/login" element={<Login />} />
              <Route path="/signup" element={<Signup />} />
            </>
          )}
        </Routes>
      </Router>
    </Fragment>
  );
}