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

const tradeSlice = createSlice({
    name: "trade",
    initialState,
    reducers: {},
    extraReducers: {
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
      [reset.fulfilled]: (state) => {
        state.success = false;
        state.trade = null;
      },
    },
  });
  
  const tradeReducer = tradeSlice.reducer;
  export default tradeReducer;