import React, { useEffect, Fragment } from "react";
import { useSelector, useDispatch } from "react-redux";
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Navigate,
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
  // const isLoggedIn = !!user;
  const isLoggedIn = false;

  useEffect(() => {
    dispatch(me());
  }, [dispatch]);

  return (
    <Fragment>
      <Navbar user={user} />
      <Router>
        <Routes>
          {isLoggedIn ? (
            <>
              <Route path="/" element={<Home />} />
              <Route path="/logTrade" element={<LogTrade />} />
              <Route path='/profile' element={<UserProfile />} />
            </>
          ) : (
            <>
              <Route path="/" element={<Navigate to="/login" />} />
              <Route path="/login" element={<Login />} />
              <Route path="/signup" element={<Signup />} />
            </>
          )}
        </Routes>
      </Router>
    </Fragment>
  );
}
