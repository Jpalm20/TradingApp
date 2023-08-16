import React, { useEffect, Fragment, useState } from "react";
import { useSelector, useDispatch } from "react-redux";
import moment from 'moment'; 
import 'moment-timezone';
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Navigate,
  Redirect
} from "react-router-dom";
import {
  Toast,
  useToast,
  Spinner
} from "@chakra-ui/react";
import { me, getTrades, getTradesPage, getUserFromSession, expiredLogout, getTradesStats, getPreferences, getAccountValues } from "./store/auth";
import Home from "./components/Home";
import PnlCalendar  from "./components/PnlCalendar";
import Login from "./components/Login";
import Signup from "./components/Signup";
import LogTrade from "./components/LogTrade";
import Navbar from "./components/Navbar";
import UserProfile from "./components/UserProfile";
import Summary from "./components/Summary";
import ResetPass from "./components/ResetPass";
import { TOKEN } from './store/auth';


export default function App() {
  const [toastMessage, setToastMessage] = useState(undefined);
  const toast = useToast();
  const dispatch = useDispatch();
  const { user } = useSelector((state) => state.auth);
  const { info } = useSelector((state) => state.auth);
  const { trades } = useSelector((state) => state.auth);
  const { stats } = useSelector((state) => state.auth);
  const authError = useSelector((state) => state.auth.error);
  const tradeError = useSelector((state) => state.trade.error);
  const tradeInfo = useSelector((state) => state.trade.info);
  const isLoggedIn = (((user && Object.keys(user).length > 2) || window.localStorage.getItem(TOKEN)) ? (true):(false));
  const [registered, setRegistered] = useState(true);
  const isRegistered = ((info && Object.keys(info).length > 2 && info.result && info.result === "User Created Successfully") ? (true):(false));
  const [deleted, setDeleted] = useState(true);
  const isDeleted = ((info && Object.keys(info).length === 1 && info.result && info.result === "User Successfully Deleted") ? (true):(false));
  const [changed, setChanged] = useState(true);
  const isChanged = ((info && Object.keys(info).length === 1 && info.result && info.result === "Password Successfully Changed") ? (true):(false));
  const [reset, setReset] = useState(true);
  const isReset = ((info && Object.keys(info).length === 1 && info.result && info.result === "Password Reset Successfully") ? (true):(false));
  const hasTrades = ((trades && trades.trades && Object.keys(trades.trades).length > 0) ? (true):(false));
  const noTrades = ((trades && trades.trades && Object.keys(trades.trades).length === 0) ? (true):(false)); 
  const hasStats = ((stats && stats.stats && Object.keys(stats.stats).length > 0) ? (true):(false));
  
  if(isRegistered === true && registered === true){
    setToastMessage(info.result);
    setRegistered(false);
  }

  if(isDeleted === true && deleted === true){
    setToastMessage(info.result);
    setDeleted(false);
  }

  if(isReset === true && reset === true){
    setToastMessage(info.result);
    setReset(false);
  }

  useEffect(() => {
    evaluateError();
  }, [authError, tradeError]); 

  const evaluateError = async () => {
    if(authError === true && info.response.data.result === "Auth Token Has Expired"){
      await dispatch(expiredLogout());
    }
    if(tradeError === true && tradeInfo.response.data.result === "Auth Token Has Expired"){
      await dispatch(expiredLogout());
    }
  }

  const returnInTZ = (utcDate) => {
    const userTZ = Intl.DateTimeFormat().resolvedOptions().timeZone;
    const tzDate = moment.utc(utcDate).tz(userTZ);
    return tzDate.format('YYYY-MM-DD')
  }

  const today = returnInTZ(new Date().toISOString());

  
  useEffect(() => {
    async function getUserTrades(){
      if(isLoggedIn && !hasTrades && !noTrades && user.user_id && !hasStats){
        const user_id = user.user_id;
        if (window.location.pathname === "/home" || window.location.pathname === "/"){
          await dispatch(getTradesStats());
          await dispatch(getPreferences());
          const filters = {};
          filters.date = today
          await dispatch(getAccountValues({ filters }));
        }else{
          const filters = {};
          filters.page = 1;
          filters.numrows = 100;
          await dispatch(getTradesPage({ filters }));
        }
      }else if (isLoggedIn && user.user_id === undefined){
        await dispatch(getUserFromSession());
      }
    }
    getUserTrades();
  }, [isLoggedIn,hasTrades,user,hasStats]);

  useEffect(() => {
    if (toastMessage) {
      toast({
        title: toastMessage,
        variant: 'solid',
        status: 'success',
        duration: 3000,
        isClosable: true
      });
    }
    setToastMessage(undefined);
  }, [toastMessage, toast]);
  
  
  return (
    <Fragment>
      <Router>
        <Navbar user={user} />
        <Routes>
          {isLoggedIn ? (
            <>
              <Route path="/" element={<Navigate to="/home"/>} />
              <Route path="/home" element={<Home user={user}/>} />
              <Route path="/PnlCalendar" element={<PnlCalendar user={user}/>} />
              <Route path="/login" element={<Navigate to="/"/>} />
              <Route path="/resetpassword" element={<Navigate to="/"/>} />
              <Route path="/signup" element={<Navigate to="/"/>} />
              <Route path="/logTrade" element={<LogTrade user={user}/>} />
              <Route path='/profile' element={<UserProfile user={user}/>} />
              <Route path='/summary' element={<Summary user={user}/>} />
            </>
          ) : (
            <>
              <Route path="/" element={<Navigate to="/login" />} />
              <Route path="/home" element={<Navigate to="/login" />} />
              <Route path="/PnlCalendar" element={<Navigate to="/login" />} />
              <Route path="/profile" element={<Navigate to="/login"/>} />
              <Route path="/logTrade" element={<Navigate to="/login"/>} />
              <Route path='/summary' element={<Navigate to="/login"/>} />
              <Route path="/login" element={<Login />} />
              <Route path="/resetpassword" element={<ResetPass />} />
              {isRegistered ? (
                <Route path="/signup" element={<Navigate to="/login"/>} />
              ) : (
                <Route path="/signup" element={<Signup />} />
              )}
            </>
          )}
        </Routes>
      </Router>
    </Fragment>
  );
}