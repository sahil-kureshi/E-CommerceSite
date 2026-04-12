import React from "react";

function CartItem({ item, removeFromCart }) {
  return (
    <div className="cart-item">
      <h4>{item.name}</h4>
      <p>Quantity: {item.quantity}</p>
      <p>Price: ₹{item.price}</p>
      <button onClick={() => removeFromCart(item.product_id)}>Remove</button>
    </div>
  );
}

export default CartItem;