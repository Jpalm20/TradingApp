import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import axios from "axios";

const TOKEN = "token";

const initialState = {
  trade: {},
  success: false,
  error: false,
  loading: false,
};

export const reset = createAsyncThunk(
  "trade/reset",
  () => ({})
);

export const create = createAsyncThunk(
  "trade/create",
  async (formInfo, { dispatch, rejectWithValue }) => {
    try {
      const { user_id, trade_type, security_type, ticker_name, expiry, strike, buy_value, units, rr, pnl, percent_wl, comments } = formInfo;
      const res = await axios.post(`http://localhost:8080/trade/create`, {
        user_id,
        trade_type,
        security_type,
        ticker_name,
        expiry,
        strike,
        buy_value,
        units,
        rr,
        pnl,
        percent_wl,
        comments
      });
      await window.localStorage.setItem(TOKEN, res.data.token)
      //dispatch(me());
      return res.data
    } catch (error) {
      console.error(error);
      return rejectWithValue(error);
    }
  }
);

export const getTrade = createAsyncThunk(
  "trade/getTrade",
  async (formInfo, { dispatch, rejectWithValue }) => {
    try {
      const { trade_id } = formInfo;
      const res = await axios.get(`http://localhost:8080/trade/${trade_id}`);
      await window.localStorage.setItem(TOKEN, res.data.token);
      //dispatch(me());
      return res.data
    } catch (error) {
      console.error(error);
      return rejectWithValue(error);
    }
  }
);

export const deleteTrade = createAsyncThunk(
  "trade/deleteTrade",
  async (formInfo, { dispatch, rejectWithValue }) => {
    try {
      const { trade_id } = formInfo;
      const res = await axios.delete(`http://localhost:8080/trade/${trade_id}`);
      await window.localStorage.setItem(TOKEN, res.data.token);
      //dispatch(me());
      return res.data
    } catch (error) {
      console.error(error);
      return rejectWithValue(error);
    }
  }
);

export const update = createAsyncThunk(
  "trade/update",
  async (formInfo, { dispatch, rejectWithValue }) => {
    try {
      const { trade_id, user_id, trade_type, security_type, ticker_name, expiry, strike, buy_value, units, rr, pnl, percent_wl, comments } = formInfo;
      const res = await axios.post(`http://localhost:8080/trade/${trade_id}`, {
        user_id,
        trade_type,
        security_type,
        ticker_name,
        expiry,
        strike,
        buy_value,
        units,
        rr,
        pnl,
        percent_wl,
        comments
      });
      await window.localStorage.setItem(TOKEN, res.data.token);
      //dispatch(me());
      return res.data
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
      },
      [getTrade.pending]: (state) => {
        state.loading = true;
      },
      [getTrade.rejected]: (state) => {
        state.error = true;
      },
      [deleteTrade.fulfilled]: (state, action) => {
        state.trade = action.payload;
        state.success = true;
      },
      [deleteTrade.pending]: (state) => {
        state.loading = true;
      },
      [deleteTrade.rejected]: (state) => {
        state.error = true;
      },
      [create.fulfilled]: (state, action) => {
        state.loading = false;
        state.success = true;
        state.trade = action.payload;
      },
      [create.pending]: (state) => {
        state.loading = true;
      },
      [create.rejected]: (state) => {
        state.error = true;
      },
      [update.fulfilled]: (state, action) => {
        state.loading = false;
        state.success = true;
        state.trade = action.payload;
      },
      [update.pending]: (state) => {
        state.loading = true;
      },
      [update.rejected]: (state) => {
        state.error = true;
      },
      [reset.fulfilled]: (state) => {
        state.success = false;
        state.trade = null;
      },
    },
  });
  
  const tradeReducer = tradeSlice.reducer;
  export default tradeReducer;