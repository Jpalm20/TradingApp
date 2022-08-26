import React, { useState } from 'react'
import { useDispatch } from 'react-redux'
import { create } from '../store/trade.js'   

export default function LogTrade() {
  const dispatch = useDispatch();
  const [trade_type, setTradeType] = useState();
  const [security_type, setSecurityType] = useState();
  const [ticker_name, setTickerName] = useState();
  const [expiry, setExpiry] = useState();
  const [strike, setStrike] = useState();
  const [buy_value, setBuyValue] = useState();
  const [units, setUnits] = useState();
  const [rr, setRR] = useState();
  const [pnl, setPNL] = useState();
  const [percent_wl, setPercentWL] = useState();
  const [comments, setComments] = useState();


  const handleSubmit = (e) => {
    e.preventDefault();
    const formName = 'logTrade';
    dispatch(create({trade_type,security_type,ticker_name,expiry,strike,buy_value,units,rr,pnl,percent_wl,comments}));
  }

  return (
    <div className='container'>
      <h1>Log A Trade</h1>
      <p>Trade Type</p>
      <input type='text' autoCapitalize='none' required onChange={(e)=>setTradeType(e.target.value)}/>
      <p>Security Type</p>
      <input type='text' autoCapitalize='none' required onChange={(e)=>setSecurityType(e.target.value)}/>
      <p>Ticker</p>
      <input type='text' autoCapitalize='none' required onChange={(e)=>setTickerName(e.target.value)}/>
      <p>Expiry (If Options, Otherwise NULL)</p>
      <input type='text' autoCapitalize='none' required onChange={(e)=>setExpiry(e.target.value)}/>
      <p>Strike Price (If Options, Otherwise 0)</p>
      <input type='text' autoCapitalize='none' required onChange={(e)=>setStrike(e.target.value)}/>
      <p>Buy Value Per Share/Contract</p>
      <input type='text' autoCapitalize='none' required onChange={(e)=>setBuyValue(e.target.value)}/>
      <p>Number of Units</p>
      <input type='text' autoCapitalize='none' required onChange={(e)=>setUnits(e.target.value)}/>
      <p>Risk/Reward</p>
      <input type='text' autoCapitalize='none' required onChange={(e)=>setRR(e.target.value)}/>
      <p>PNL</p>
      <input type='text' autoCapitalize='none' required onChange={(e)=>setPNL(e.target.value)}/>
      <p>Percent Win or Loss</p>
      <input type='text' autoCapitalize='none' required onChange={(e)=>setPercentWL(e.target.value)}/>
      <p>Comments</p>
      <input type='text' autoCapitalize='none' required onChange={(e)=>setComments(e.target.value)}/>
      <button className='submit' onClick={handleSubmit}>Submit</button>
    </div>
  )
}
