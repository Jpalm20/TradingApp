import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import axios from "axios";

const TOKEN = "";

const initialState = {
  trades: [],
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
    const res = await axios.get("http://localhost:8080/", {
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
      const res = await axios.post(`http://localhost:8080/user/register`, {
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
      const res = await axios.post(`http://localhost:8080/user/login`, {
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
        const res = await axios.post(`http://localhost:8080/user/${user_id}`, {
          headers: {
            Authorization: "Bearer " + token,
          },
          first_name,
          last_name,
          email,
          street_address,
          city,
          state,
          country
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
        const res = await axios.get(`http://localhost:8080/user/trades/${user_id}`,{
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

export const getPnlByYear = createAsyncThunk(
  "auth/getPnlByYear",
  async (formInfo, { dispatch, rejectWithValue }) => {
    const token = await window.localStorage.getItem(TOKEN);
    try {
      if (token) {
        const { user_id, year } = formInfo;
        const res = await axios.get(`http://localhost:8080/user/pnlbyYear/${user_id}/${year}`,{
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

export const deleteUser = createAsyncThunk(
  "auth/deleteUser",
  async (formInfo, { dispatch, rejectWithValue }) => {
    const token = await window.localStorage.getItem(TOKEN);
    try {
      if (token) {
        const { user_id } = formInfo;
        const res = await axios.delete(`http://localhost:8080/user/${user_id}`,{
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
    },
    [getPnlByYear.fulfilled]: (state, action) => {
      state.pnlYTD = action.payload;
      state.success = true;
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
    },
    [deleteUser.fulfilled]: (state, action) => {
      state.loading = false;
      state.success = false;
      state.user = null;
      state.trades = null;
      state.pnlYTD = null;
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
    },
    [logout.fulfilled]: (state) => {
      state.success = false;
      state.user = null;
      state.trades = null;
      state.pnlYTD = null;
      state.info = null;
      state.error = false;
    },
  },
});

const authReducer = authSlice.reducer;
export default authReducer;
