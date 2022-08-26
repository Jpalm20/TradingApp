import React, { useEffect } from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { useSelector, useDispatch } from "react-redux";
import { me } from "./store/auth";
import Home from "./components/Home";
import Login from "./components/Login";
import Signup from "./components/Signup";
import LogTrade from "./components/LogTrade";


export default function App() {
/*  const dispatch = useDispatch();
  const { user } = useSelector((state) => state.auth);
  const isLoggedIn = !!user;

  useEffect(() => {
    dispatch(me());
  }, []);
*/
  return (
    <Router>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/signup" element={<Signup />} />
          <Route path="/logTrade" element={<LogTrade />} />
        </Routes>
    </Router>
  );
}
