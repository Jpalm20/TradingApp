import { configureStore } from "@reduxjs/toolkit";
import authReducer from "./auth";
import tradeReducer from "./trade";
// import reducers

export default configureStore({
  reducer: {
    auth: authReducer,
    trade: tradeReducer
  }
})
