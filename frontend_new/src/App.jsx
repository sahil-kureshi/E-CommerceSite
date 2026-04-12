import React from "react";
import AppRouter from "./router/AppRouter.jsx";
import { CartProvider } from "./context/CartContext.jsx";

function App() {
  return (
    <CartProvider>
      <AppRouter />
    </CartProvider>
  );
}

export default App;