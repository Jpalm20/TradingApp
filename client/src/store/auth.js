import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import axios from "axios";
import Summary from '../components/Summary'

const TOKEN = "token";
export { TOKEN };
const API_URL = process.env.REACT_APP_API_URL;

const initialState = {
  trades: [],
  stats: {},
  preferences: {},
  accountValues: {},
  tradesOfDay: [],
  pnlYTD: {},
  user: {},
  success: false,
  error: false,
  loading: false,
  info: {},
};

export const me = createAsyncThunk("auth/me", async () => {
  const token = await window.localStorage.getItem(TOKEN);
  if (token) {
    const res = await axios.get(API_URL, {
      headers: {
        Authorization: "Bearer " + token,
      },
    });
    return res.data;
  }
});

export const register = createAsyncThunk(
  "auth/register",
  async (formInfo, { dispatch, rejectWithValue }) => {
    try {
      const { first_name, last_name, birthday, email, password, street_address, city, state, country } = formInfo;
      const res = await axios.post(API_URL + `user/register`, {
        first_name,
        last_name,
        birthday,
        email,
        password,
        street_address,
        city,
        state,
        country
      });
      //dispatch(me());
      return res.data
    } catch (error) {
      console.error(error);
      return rejectWithValue(error);
    }
  }
);

export const authenticate = createAsyncThunk(
  "auth/authenticate",
  async (formInfo, { dispatch, rejectWithValue }) => {
    try {
      const { email, password } = formInfo;
      const res = await axios.post(API_URL + `user/login`, {
        email,
        password,
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

export const update = createAsyncThunk(
  "auth/update",
  async (formInfo, { dispatch, rejectWithValue }) => {
    const token = await window.localStorage.getItem(TOKEN);
    try {
      if (token) {
        const { first_name, last_name, email, street_address, city, state, country } = formInfo;
        const res = await axios.post(API_URL + `user`, {
          first_name,
          last_name,
          email,
          street_address,
          city,
          state,
          country
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

export const getPreferences = createAsyncThunk(
  "auth/getPreferences",
  async (formInfo, { dispatch, rejectWithValue }) => {
    const token = await window.localStorage.getItem(TOKEN);
    try {
      if (token) {
        const res = await axios.get(API_URL + `user/preferences`,{
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

export const getAccountValues = createAsyncThunk(
  "auth/getAccountValues",
  async (formInfo, { dispatch, rejectWithValue }) => {
    const token = await window.localStorage.getItem(TOKEN);
    try {
      if (token) {
        const res = await axios.get(API_URL + `user/accountValue`,{
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

export const getTrades = createAsyncThunk(
  "auth/getTrades",
  async (formInfo, { dispatch, rejectWithValue }) => {
    const token = await window.localStorage.getItem(TOKEN);
    try {
      if (token) {
        const res = await axios.get(API_URL + `user/trades`,{
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

export const getTradesFiltered = createAsyncThunk(
  "auth/getTradesFiltered",
  async (formInfo, { dispatch, rejectWithValue }) => {
    const token = await window.localStorage.getItem(TOKEN);
    try {
      if (token) {
        const { filters } = formInfo;
        const res = await axios.get(API_URL + `user/trades`,{
          headers: {
            Authorization: "Bearer " + token,
          },
          params: filters
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

export const getTradesStats = createAsyncThunk(
  "auth/getTradesStats",
  async (formInfo, { dispatch, rejectWithValue }) => {
    const token = await window.localStorage.getItem(TOKEN);
    try {
      if (token) {
        const res = await axios.get(API_URL + `user/trades/stats`,{
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

export const getTradesStatsFiltered = createAsyncThunk(
  "auth/getTradesStatsFiltered",
  async (formInfo, { dispatch, rejectWithValue }) => {
    const token = await window.localStorage.getItem(TOKEN);
    try {
      if (token) {
        const { filters } = formInfo;
        const res = await axios.get(API_URL + `user/trades/stats`,{
          headers: {
            Authorization: "Bearer " + token,
          },
          params: filters
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

export const getTradesPage = createAsyncThunk(
  "auth/getTradesPage",
  async (formInfo, { dispatch, rejectWithValue }) => {
    const token = await window.localStorage.getItem(TOKEN);
    try {
      if (token) {
        const { filters } = formInfo;
        const res = await axios.get(API_URL + `user/trades/page`,{
          headers: {
            Authorization: "Bearer " + token,
          },
          params: filters
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

export const getTradesOfDateFiltered = createAsyncThunk(
  "auth/getTradesOfDateFiltered",
  async (formInfo, { dispatch, rejectWithValue }) => {
    const token = await window.localStorage.getItem(TOKEN);
    try {
      if (token) {
        const { filters } = formInfo;
        const res = await axios.get(API_URL + `user/trades`,{
          headers: {
            Authorization: "Bearer " + token,
          },
          params: filters
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

export const getPnlByYear = createAsyncThunk(
  "auth/getPnlByYear",
  async (formInfo, { dispatch, rejectWithValue }) => {
    const token = await window.localStorage.getItem(TOKEN);
    try {
      if (token) {
        const { year } = formInfo;
        const res = await axios.get(API_URL + `user/pnlbyYear/${year}`,{
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

export const getPnlByYearFiltered = createAsyncThunk(
  "auth/getPnlByYearFiltered",
  async (formInfo, { dispatch, rejectWithValue }) => {
    const token = await window.localStorage.getItem(TOKEN);
    try {
      if (token) {
        const { year, filters } = formInfo;
        const res = await axios.get(API_URL + `user/pnlbyYear/${year}`,{
          headers: {
            Authorization: "Bearer " + token,
          },
          params: filters
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

export const deleteUser = createAsyncThunk(
  "auth/deleteUser",
  async (formInfo, { dispatch, rejectWithValue }) => {
    const token = await window.localStorage.getItem(TOKEN);
    try {
      if (token) {
        const res = await axios.delete(API_URL + `user`,{
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


export const toggleAvTracking = createAsyncThunk(
  "auth/toggleAvTracking",
  async (formInfo, { dispatch, rejectWithValue }) => {
    const token = await window.localStorage.getItem(TOKEN);
    try {
      if (token) {
        const res = await axios.post(API_URL + `user/preferences/toggleav`,{  
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


export const changePassword = createAsyncThunk(
  "auth/changePassword",
  async (formInfo, { dispatch, rejectWithValue }) => {
    const token = await window.localStorage.getItem(TOKEN);
    try {
      if (token) {
        const { curr_pass, new_pass_1, new_pass_2 } = formInfo;
        const res = await axios.post(API_URL + `user/changePassword`,{
          curr_pass,
          new_pass_1,
          new_pass_2
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


export const setAccountValue = createAsyncThunk(
  "auth/setAccountValue",
  async (formInfo, { dispatch, rejectWithValue }) => {
    const token = await window.localStorage.getItem(TOKEN);
    try {
      if (token) {
        const { accountvalue } = formInfo;
        const res = await axios.post(API_URL + `user/accountValue`,{
          accountvalue
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


export const generateResetCode = createAsyncThunk(
  "auth/generateResetCode",
  async (formInfo, { dispatch, rejectWithValue }) => {
    try {
        const { email } = formInfo;
        const res = await axios.post(API_URL + `user/generateResetCode`,{
          email
        });
        //await window.localStorage.setItem(TOKEN, res.data.token);
        //dispatch(me());
        return res.data
    } catch (error) {
      console.error(error);
      return rejectWithValue(error);
    }
  }
);


export const confirmResetCode = createAsyncThunk(
  "auth/confirmResetCode",
  async (formInfo, { dispatch, rejectWithValue }) => {
    try {
        const { email, code } = formInfo;
        const res = await axios.post(API_URL + `user/confirmResetCode`,{
          email,
          code
        });
        //await window.localStorage.setItem(TOKEN, res.data.token);
        //dispatch(me());
        return res.data
    } catch (error) {
      console.error(error);
      return rejectWithValue(error);
    }
  }
);


export const resetPassword = createAsyncThunk(
  "auth/resetPassword",
  async (formInfo, { dispatch, rejectWithValue }) => {
    try {
        const { code, email, new_pass_1, new_pass_2 } = formInfo;
        const res = await axios.post(API_URL + `user/resetPassword`,{
          code,
          email,
          new_pass_1,
          new_pass_2
        });
        //await window.localStorage.setItem(TOKEN, res.data.token);
        //dispatch(me());
        return res.data
    } catch (error) {
      console.error(error);
      return rejectWithValue(error);
    }
  }
);


export const reportBug = createAsyncThunk(
  "auth/reportBug",
  async (formInfo, { dispatch, rejectWithValue }) => {
    const token = await window.localStorage.getItem(TOKEN);
    try {
      if (token) {
        const { requestType, summary, description, page } = formInfo;
        const res = await axios.post(API_URL + `user/reportBug`,{
          requestType,
          summary,
          description,
          page
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


export const logout = createAsyncThunk(
  "auth/logout", 
  async (formInfo, { dispatch, rejectWithValue }) => {
    const token = await window.localStorage.getItem(TOKEN);
    try {
      if (token) {
        const res = await axios.post(API_URL + `user/logout`,{
          
        },{
          headers: {
            Authorization: "Bearer " + token,
          }
        });
        await window.localStorage.removeItem(TOKEN);
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

export const expiredLogout = createAsyncThunk("auth/expiredLogout", async () => {
  await window.localStorage.removeItem(TOKEN);
});

export const getUserFromSession = createAsyncThunk(
  "auth/getUserFromSession", 
  async (formInfo, { dispatch, rejectWithValue }) => {
    const token = await window.localStorage.getItem(TOKEN);
    try {
      if (token) {
        const res = await axios.get(API_URL + `user/getUserFromSession`,{
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

const authSlice = createSlice({
  name: "auth",
  initialState,
  reducers: {},
  extraReducers: {
    [me.fulfilled]: (state, action) => {
      state.user = action.payload;
      state.success = true;
      state.error = false;
    },
    [getPreferences.fulfilled]: (state, action) => {
      state.preferences = action.payload;
      state.success = true;
      state.loading = false;
      state.info = null;
      state.error = false;
    },
    [getPreferences.pending]: (state) => {
      state.loading = true;
      state.error = false;
      state.success = false;
    },
    [getPreferences.rejected]: (state, action) => {
      state.error = true;
      state.info = action.payload;
      state.loading = false;
    },
    [toggleAvTracking.fulfilled]: (state, action) => {
      state.preferences = action.payload;
      state.success = true;
      state.loading = false;
      state.info = null;
      state.error = false;
    },
    [toggleAvTracking.pending]: (state) => {
      state.loading = true;
      state.error = false;
      state.success = false;
    },
    [toggleAvTracking.rejected]: (state, action) => {
      state.error = true;
      state.info = action.payload;
      state.loading = false;
    },
    [getAccountValues.fulfilled]: (state, action) => {
      state.accountValues = action.payload;
      state.success = true;
      state.loading = false;
      state.info = null;
      state.error = false;
    },
    [getAccountValues.pending]: (state) => {
      state.loading = true;
      state.error = false;
      state.success = false;
    },
    [getAccountValues.rejected]: (state, action) => {
      state.error = true;
      state.info = action.payload;
      state.loading = false;
    },
    [getTrades.fulfilled]: (state, action) => {
      state.trades = action.payload;
      state.success = true;
      state.loading = false;
      state.info = null;
      state.error = false;
    },
    [getTrades.pending]: (state) => {
      state.loading = true;
      state.error = false;
      state.success = false;
    },
    [getTrades.rejected]: (state, action) => {
      state.error = true;
      state.info = action.payload;
      state.loading = false;
    },
    [getTradesFiltered.fulfilled]: (state, action) => {
      state.trades = action.payload;
      state.success = true;
      state.loading = false;
      state.info = null;
      state.error = false;
    },
    [getTradesFiltered.pending]: (state) => {
      state.loading = true;
      state.error = false;
      state.success = false;
    },
    [getTradesFiltered.rejected]: (state, action) => {
      state.error = true;
      state.info = action.payload;
      state.loading = false;
    },
    [getTradesStats.fulfilled]: (state, action) => {
      state.stats = action.payload;
      state.success = true;
      state.loading = false;
      state.info = null;
      state.error = false;
    },
    [getTradesStats.pending]: (state) => {
      state.loading = true;
      state.error = false;
      state.success = false;
    },
    [getTradesStats.rejected]: (state, action) => {
      state.error = true;
      state.info = action.payload;
      state.loading = false;
    },
    [getTradesStatsFiltered.fulfilled]: (state, action) => {
      state.stats = action.payload;
      state.success = true;
      state.loading = false;
      state.info = null;
      state.error = false;
    },
    [getTradesStatsFiltered.pending]: (state) => {
      state.loading = true;
      state.error = false;
      state.success = false;
    },
    [getTradesStatsFiltered.rejected]: (state, action) => {
      state.error = true;
      state.info = action.payload;
      state.loading = false;
    },
    [getTradesOfDateFiltered.fulfilled]: (state, action) => {
      state.tradesOfDay = action.payload;
      state.success = true;
      state.loading = false;
      state.info = null;
      state.error = false;
    },
    [getTradesOfDateFiltered.pending]: (state) => {
      state.loading = true;
      state.error = false;
      state.success = false;
    },
    [getTradesOfDateFiltered.rejected]: (state, action) => {
      state.error = true;
      state.info = action.payload;
      state.loading = false;
    },
    [getPnlByYear.fulfilled]: (state, action) => {
      state.pnlYTD = action.payload;
      state.success = true;
      state.loading = false;
      state.info = null;
      state.error = false;
    },
    [getPnlByYear.pending]: (state) => {
      state.loading = true;
      state.error = false;
      state.success = false;
    },
    [getPnlByYear.rejected]: (state, action) => {
      state.error = true;
      state.info = action.payload;
      state.loading = false;
    },
    [getPnlByYearFiltered.fulfilled]: (state, action) => {
      state.pnlYTD = action.payload;
      state.success = true;
      state.loading = false;
      state.info = null;
      state.error = false;
    },
    [getPnlByYearFiltered.pending]: (state) => {
      state.loading = true;
      state.error = false;
      state.success = false;
    },
    [getPnlByYearFiltered.rejected]: (state, action) => {
      state.error = true;
      state.info = action.payload;
      state.loading = false;
    },
    [register.fulfilled]: (state, action) => {
      state.loading = false;
      state.success = true;
      state.info = action.payload;
      state.error = false;
    },
    [register.pending]: (state) => {
      state.loading = true;
      state.error = false;
      state.success = false;
    },
    [register.rejected]: (state, action) => {
      state.error = true;
      state.info = action.payload;
      state.loading = false;
    },
    [authenticate.fulfilled]: (state, action) => {
      state.loading = false;
      state.success = true;
      state.user = action.payload;
      state.info = null;
      state.error = false;
    },
    [authenticate.pending]: (state) => {
      state.loading = true;
      state.error = false;
      state.success = false;
    },
    [authenticate.rejected]: (state, action) => {
      state.error = true;
      state.info = action.payload;
      state.loading = false;
    },
    [getUserFromSession.fulfilled]: (state, action) => {
      state.loading = false;
      state.success = true;
      state.user = action.payload;
      state.info = null;
      state.error = false;
    },
    [getUserFromSession.pending]: (state) => {
      state.loading = true;
      state.error = false;
      state.success = false;
    },
    [getUserFromSession.rejected]: (state, action) => {
      state.error = true;
      state.info = action.payload;
      state.loading = false;
    },
    [update.fulfilled]: (state, action) => {
      state.loading = false;
      state.success = true;
      state.user = action.payload;
      state.info = null;
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
    [changePassword.fulfilled]: (state, action) => {
      state.loading = false;
      state.success = true;
      state.info = action.payload;
      state.error = false;
    },
    [changePassword.pending]: (state) => {
      state.loading = true;
      state.error = false;
      state.success = false;
    },
    [changePassword.rejected]: (state, action) => {
      state.error = true;
      state.info = action.payload;
      state.loading = false;
    },
    [setAccountValue.fulfilled]: (state, action) => {
      state.loading = false;
      state.success = true;
      state.info = action.payload;
      state.error = false;
    },
    [setAccountValue.pending]: (state) => {
      state.loading = true;
      state.error = false;
      state.success = false;
    },
    [setAccountValue.rejected]: (state, action) => {
      state.error = true;
      state.info = action.payload;
      state.loading = false;
    },
    [deleteUser.fulfilled]: (state, action) => {
      state.loading = false;
      state.success = true;
      state.trades = null;
      state.pnlYTD = null;
      state.tradesOfDay = null;
      state.info = action.payload;
      state.error = false;
    },
    [deleteUser.pending]: (state) => {
      state.loading = true;
      state.error = false;
      state.success = false;
    },
    [deleteUser.rejected]: (state, action) => {
      state.error = true;
      state.info = action.payload;
      state.loading = false;
    },
    [reportBug.fulfilled]: (state, action) => {
      state.loading = false;
      state.success = true;
      state.info = action.payload;
      state.error = false;
    },
    [reportBug.pending]: (state) => {
      state.loading = true;
      state.error = false;
      state.success = false;
    },
    [reportBug.rejected]: (state, action) => {
      state.error = true;
      state.info = action.payload;
      state.loading = false;
    },
    [logout.fulfilled]: (state) => {
      state.success = true;
      state.user = null;
      state.trades = null;
      state.stats = null;
      state.preferences = null;
      state.accountValues = null;
      state.tradesOfDay = null;
      state.pnlYTD = null;
      state.info = null;
      state.error = false;
      state.loading = false;
    },
    [logout.rejected]: (state, action) => {
      state.error = true;
      state.info = action.payload;
      state.loading = false;
    },
    [logout.pending]: (state) => {
      state.success = false;
      state.error = false;
      state.loading = true;
    },
    [expiredLogout.fulfilled]: (state) => {
      state.success = true;
      state.user = null;
      state.trades = null;
      state.stats = null;
      state.preferences = null;
      state.accountValues = null;
      state.tradesOfDay = null;
      state.pnlYTD = null;
      state.info = null;
      state.error = false;
      state.loading = false;
    },
    [resetPassword.fulfilled]: (state, action) => {
      state.loading = false;
      state.success = true;
      state.info = action.payload;
      state.error = false;
    },
    [resetPassword.pending]: (state) => {
      state.loading = true;
      state.error = false;
      state.success = false;
    },
    [resetPassword.rejected]: (state, action) => {
      state.error = true;
      state.info = action.payload;
      state.loading = false;
    },
    [generateResetCode.fulfilled]: (state, action) => {
      state.loading = false;
      state.success = true;
      state.info = action.payload;
      state.error = false;
    },
    [generateResetCode.pending]: (state) => {
      state.loading = true;
      state.error = false;
      state.success = false;
    },
    [generateResetCode.rejected]: (state, action) => {
      state.error = true;
      state.info = action.payload;
      state.loading = false;
    },
    [confirmResetCode.fulfilled]: (state, action) => {
      state.loading = false;
      state.success = true;
      state.info = action.payload;
      state.error = false;
    },
    [confirmResetCode.pending]: (state) => {
      state.loading = true;
      state.error = false;
      state.success = false;
    },
    [confirmResetCode.rejected]: (state, action) => {
      state.error = true;
      state.info = action.payload;
      state.loading = false;
    },
    [getTradesPage.fulfilled]: (state, action) => {
      state.trades = action.payload;
      state.success = true;
      state.loading = false;
      state.info = null;
      state.error = false;
    },
    [getTradesPage.pending]: (state) => {
      state.loading = true;
      state.error = false;
      state.success = false;
    },
    [getTradesPage.rejected]: (state, action) => {
      state.error = true;
      state.info = action.payload;
      state.loading = false;
    },
  },
});

const authReducer = authSlice.reducer;
export default authReducer;
