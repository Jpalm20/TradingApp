import { configureStore } from "@reduxjs/toolkit";
import authReducer from "./auth";
// import reducers

export default configureStore({
  reducer: {
    auth: authReducer
  }
})
