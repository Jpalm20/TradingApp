import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import axios from "axios";

const TOKEN = "token";

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
  const token = await window.localStorage.getItem(TOKEN)
  if (token) {
    const res = await axios.get("http://localhost:8080/", {
      headers: {
        authorization: token,
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
      await window.localStorage.setItem(TOKEN, res.data.token)
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
    try {
      const { user_id, first_name, last_name, email, street_address, city, state, country } = formInfo;
      const res = await axios.post(`http://localhost:8080/user/${user_id}`, {
        first_name,
        last_name,
        email,
        street_address,
        city,
        state,
        country
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

export const getTrades = createAsyncThunk(
  "auth/getTrades",
  async (formInfo, { dispatch, rejectWithValue }) => {
    try {
      const { user_id } = formInfo;
      const res = await axios.get(`http://localhost:8080/user/trades/${user_id}`);
      await window.localStorage.setItem(TOKEN, res.data.token);
      //dispatch(me());
      return res.data
    } catch (error) {
      console.error(error);
      return rejectWithValue(error);
    }
  }
);

export const getPnlByYear = createAsyncThunk(
  "auth/getPnlByYear",
  async (formInfo, { dispatch, rejectWithValue }) => {
    try {
      const { user_id, year } = formInfo;
      const res = await axios.get(`http://localhost:8080/user/pnlbyYear/${user_id}/${year}`);
      await window.localStorage.setItem(TOKEN, res.data.token);
      //dispatch(me());
      return res.data
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
    },
    [getTrades.fulfilled]: (state, action) => {
      state.trades = action.payload;
      state.success = true;
    },
    [getTrades.pending]: (state) => {
      state.loading = true;
    },
    [getTrades.rejected]: (state, action) => {
      state.error = true;
      state.info = action.payload;
    },
    [getPnlByYear.fulfilled]: (state, action) => {
      state.pnlYTD = action.payload;
      state.success = true;
    },
    [getPnlByYear.pending]: (state) => {
      state.loading = true;
    },
    [getPnlByYear.rejected]: (state, action) => {
      state.error = true;
      state.info = action.payload;
    },
    [register.fulfilled]: (state, action) => {
      state.loading = false;
      state.success = true;
      state.info = action.payload;
    },
    [register.pending]: (state) => {
      state.loading = true;
    },
    [register.rejected]: (state, action) => {
      state.error = true;
      state.info = action.payload;
    },
    [authenticate.fulfilled]: (state, action) => {
      state.loading = false;
      state.success = true;
      state.user = action.payload;
    },
    [authenticate.pending]: (state) => {
      state.loading = true;
    },
    [authenticate.rejected]: (state, action) => {
      state.error = true;
      state.info = action.payload;
    },
    [update.fulfilled]: (state, action) => {
      state.loading = false;
      state.success = true;
      state.user = action.payload;
    },
    [update.pending]: (state) => {
      state.loading = true;
    },
    [update.rejected]: (state, action) => {
      state.error = true;
      state.info = action.payload;
    },
    [logout.fulfilled]: (state) => {
      state.success = false;
      state.user = null;
      state.trades = null;
      state.pnlYTD = null;
      state.info = null;
    },
  },
});

const authReducer = authSlice.reducer;
export default authReducer;
