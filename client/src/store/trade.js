import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import axios from "axios";
import { TOKEN } from './auth';

const API_URL = process.env.REACT_APP_API_URL;

const initialState = {
  trade: {},
  success: false,
  error: false,
  loading: false,
  info: {},
};

export const reset = createAsyncThunk(
  "trade/reset",
  () => ({})
);

export const create = createAsyncThunk(
  "trade/create",
  async (formInfo, { dispatch, rejectWithValue }) => {
    const token = await window.localStorage.getItem(TOKEN);
    try {
      if (token) {
        const { user_id, trade_type, security_type, ticker_name, trade_date, expiry, strike, buy_value, units, rr, pnl, percent_wl, comments } = formInfo;
        const res = await axios.post(API_URL + `trade/create`, {
          user_id,
          trade_type,
          security_type,
          ticker_name,
          trade_date,
          expiry,
          strike,
          buy_value,
          units,
          rr,
          pnl,
          percent_wl,
          comments
        },{
          headers: {
            Authorization: "Bearer " + token,
          }
        });
        //await window.localStorage.setItem(TOKEN, res.data.token)
        //dispatch(me());
        return res.data
      }
    } catch (error) {
      console.error(error);
      return rejectWithValue(error);
    }
  }
);

export const getTrade = createAsyncThunk(
  "trade/getTrade",
  async (formInfo, { dispatch, rejectWithValue }) => {
    const token = await window.localStorage.getItem(TOKEN);
    try {
      if (token) {
        const { trade_id } = formInfo;
        const res = await axios.get(API_URL + `trade/${trade_id}`,{
          headers: {
            Authorization: "Bearer " + token,
          }
        });
        //await window.localStorage.setItem(TOKEN, res.data.token);
        //dispatch(me());
        return res.data
      }
    } catch (error) {
      console.error(error);
      return rejectWithValue(error);
    }
  }
);

export const deleteTrade = createAsyncThunk(
  "trade/deleteTrade",
  async (formInfo, { dispatch, rejectWithValue }) => {
    const token = await window.localStorage.getItem(TOKEN);
    try {
      if (token) {
        const { trade_id } = formInfo;
        const res = await axios.delete(API_URL + `trade/${trade_id}`,{
          headers: {
            Authorization: "Bearer " + token,
          }
        });
        //await window.localStorage.setItem(TOKEN, res.data.token);
        //dispatch(me());
        return res.data
      }
    } catch (error) {
      console.error(error);
      return rejectWithValue(error);
    }
  }
);

export const update = createAsyncThunk(
  "trade/update",
  async (formInfo, { dispatch, rejectWithValue }) => {
    const token = await window.localStorage.getItem(TOKEN);
    try {
      if (token) {
        const { trade_id, user_id, trade_type, security_type, ticker_name, trade_date, expiry, strike, buy_value, units, rr, pnl, percent_wl, comments } = formInfo;
        const res = await axios.post(API_URL + `trade/${trade_id}`, {
          user_id,
          trade_type,
          security_type,
          ticker_name,
          trade_date,
          expiry,
          strike,
          buy_value,
          units,
          rr,
          pnl,
          percent_wl,
          comments
        },{
          headers: {
            Authorization: "Bearer " + token,
          }
        });
        //await window.localStorage.setItem(TOKEN, res.data.token);
        //dispatch(me());
        return res.data
      }
    } catch (error) {
      console.error(error);
      return rejectWithValue(error);
    }
  }
);

const tradeSlice = createSlice({
    name: "trade",
    initialState,
    reducers: {},
    extraReducers: {
      [getTrade.fulfilled]: (state, action) => {
        state.trade = action.payload;
        state.success = true;
        state.error = false;
        state.loading = false;
      },
      [getTrade.pending]: (state) => {
        state.loading = true;
        state.error = false;
        state.success = false;
      },
      [getTrade.rejected]: (state, action) => {
        state.error = true;
        state.info = action.payload;
        state.loading = false;
      },
      [deleteTrade.fulfilled]: (state, action) => {
        state.trade = action.payload;
        state.success = true;
        state.error = false;
        state.loading = false;
      },
      [deleteTrade.pending]: (state) => {
        state.loading = true;
        state.error = false;
        state.success = false;
      },
      [deleteTrade.rejected]: (state, action) => {
        state.error = true;
        state.info = action.payload;
        state.loading = false;
      },
      [create.fulfilled]: (state, action) => {
        state.loading = false;
        state.success = true;
        state.trade = action.payload;
        state.error = false;
      },
      [create.pending]: (state) => {
        state.loading = true;
        state.error = false;
        state.success = false;
      },
      [create.rejected]: (state, action) => {
        state.error = true;
        state.info = action.payload;
        state.loading = false;
      },
      [update.fulfilled]: (state, action) => {
        state.loading = false;
        state.success = true;
        state.trade = action.payload;
        state.error = false;
      },
      [update.pending]: (state) => {
        state.loading = true;
        state.error = false;
        state.success = false;
      },
      [update.rejected]: (state, action) => {
        state.error = true;
        state.info = action.payload;
        state.loading = false;
      },
      [reset.fulfilled]: (state) => {
        state.success = false;
        state.trade = null;
        state.loading = false;
      },
    },
  });
  
  const tradeReducer = tradeSlice.reducer;
  export default tradeReducer;
