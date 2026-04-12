import React, { useContext } from "react";
import { CartContext } from "../context/CartContext";
import CartItem from "../components/CartItem";
import { useNavigate } from "react-router-dom";

function Cart() {
  const { cart, removeFromCart } = useContext(CartContext);
  const navigate = useNavigate();

  const total = cart.reduce((sum, item) => sum + item.price * item.quantity, 0);

  if (cart.length === 0) return <p>Your cart is empty.</p>;

  return (
    <div>
      <h2>My Cart</h2>
      {cart.map((item) => (
        <CartItem key={item.product_id} item={item} removeFromCart={removeFromCart} />
      ))}
      <h3>Total: ₹{total}</h3>
      <button onClick={() => navigate("/checkout")}>Proceed to Checkout</button>
    </div>
  );
}

export default Cart;