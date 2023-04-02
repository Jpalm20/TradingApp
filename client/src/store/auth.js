import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import axios from "axios";
import Summary from '../components/Summary'

const TOKEN = "";
const API_URL = process.env.REACT_APP_API_URL;

const initialState = {
  trades: [],
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
        const { user_id, first_name, last_name, email, street_address, city, state, country } = formInfo;
        const res = await axios.post(API_URL + `user/${user_id}`, {
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

export const getTrades = createAsyncThunk(
  "auth/getTrades",
  async (formInfo, { dispatch, rejectWithValue }) => {
    const token = await window.localStorage.getItem(TOKEN);
    try {
      if (token) {
        const { user_id } = formInfo;
        const res = await axios.get(API_URL + `user/trades/${user_id}`,{
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
        const { user_id, filters } = formInfo;
        const res = await axios.get(API_URL + `user/trades/${user_id}`,{
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
        const { user_id, filters } = formInfo;
        const res = await axios.get(API_URL + `user/trades/${user_id}`,{
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
        const { user_id, year } = formInfo;
        const res = await axios.get(API_URL + `user/pnlbyYear/${user_id}/${year}`,{
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
        const { user_id, year, filters } = formInfo;
        const res = await axios.get(API_URL + `user/pnlbyYear/${user_id}/${year}`,{
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
        const { user_id } = formInfo;
        const res = await axios.delete(API_URL + `user/${user_id}`,{
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
        const { user_id, curr_pass, new_pass_1, new_pass_2 } = formInfo;
        const res = await axios.post(API_URL + `user/changePassword/${user_id}`,{
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


export const reportBug = createAsyncThunk(
  "auth/reportBug",
  async (formInfo, { dispatch, rejectWithValue }) => {
    const token = await window.localStorage.getItem(TOKEN);
    try {
      if (token) {
        const { summary, description, page } = formInfo;
        const res = await axios.post(API_URL + `user/reportBug`,{
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


export const logout = createAsyncThunk("auth/logout", async () => {
  await window.localStorage.removeItem(TOKEN);
});

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
    [deleteUser.fulfilled]: (state, action) => {
      state.loading = false;
      state.success = false;
      state.user = null;
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
      state.success = false;
      state.user = null;
      state.trades = null;
      state.tradesOfDay = null;
      state.pnlYTD = null;
      state.info = null;
      state.error = false;
    },
  },
});

const authReducer = authSlice.reducer;
export default authReducer;
