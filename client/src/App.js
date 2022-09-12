import React, { useEffect, Fragment } from "react";
import { useSelector, useDispatch } from "react-redux";
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Navigate,
  Redirect
} from "react-router-dom";
import { me } from "./store/auth";
import Home from "./components/Home";
import Login from "./components/Login";
import Signup from "./components/Signup";
import LogTrade from "./components/LogTrade";
import Navbar from "./components/Navbar";
import UserProfile from "./components/UserProfile";

export default function App() {
  const dispatch = useDispatch();
  const { user } = useSelector((state) => state.auth);
  const isLoggedIn = ((user && Object.keys(user).length > 2) ? (true):(false));
  
  /*
  useEffect(() => {
    dispatch(me());
  }, [dispatch]);
  */
  
  return (
    <Fragment>
      <Router>
        <Navbar user={user} />
        <Routes>
          {isLoggedIn ? (
            <>
              <Route path="/" element={<Home />} />
              <Route path="/login" element={<Navigate to="/profile"/>} />
              <Route path="/signup" element={<Navigate to="/profile"/>} />
              <Route path="/logTrade" element={<LogTrade user={user}/>} />
              <Route path='/profile' element={<UserProfile user={user}/>} />
            </>
          ) : (
            <>
              <Route path="/" element={<Navigate to="/login" />} />
              <Route path="/profile" element={<Navigate to="/login"/>} />
              <Route path="/logTrade" element={<Navigate to="/login"/>} />
              <Route path="/login" element={<Login />} />
              <Route path="/signup" element={<Signup />} />
            </>
          )}
        </Routes>
      </Router>
    </Fragment>
  );
}