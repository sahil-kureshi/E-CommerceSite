import React, { useContext } from "react";
import { CartContext } from "../context/CartContext";
import CheckoutButton from "../components/CheckoutButton";
import { createOrder } from "../api/ordersApi";

function Checkout() {
  const { cart, clearCart } = useContext(CartContext);

  const total = cart.reduce((sum, item) => sum + item.price * item.quantity, 0);

  const handleOrder = async () => {
    const orderData = {
      customer_id: 1, // Replace with logged-in user ID
      items: cart.map((item) => ({
        product_id: item.product_id,
        quantity: item.quantity,
        price: item.price,
      })),
    };

    const order = await createOrder(orderData);
    clearCart();
    return order.order_id;
  };

  return (
    <div>
      <h2>Checkout</h2>
      <p>Total Amount: ₹{total}</p>
      <CheckoutButton orderId={1} amount={total} /> {/* Replace with dynamic orderId */}
    </div>
  );
}

export default Checkout;