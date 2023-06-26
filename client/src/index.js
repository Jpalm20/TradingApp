import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";
import { Provider } from "react-redux";
import { ChakraProvider } from "@chakra-ui/react";
import store from "./store";
import { ColorModeScript } from '@chakra-ui/react'
import theme from './theme'


const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
  <React.StrictMode>
    <Provider store={store}>
      <ChakraProvider>
        <ColorModeScript initialColorMode={theme.config.initialColorMode} />
        <App />
      </ChakraProvider>
    </Provider>
  </React.StrictMode>
);
