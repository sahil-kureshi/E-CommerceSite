import React from "react";
import { createPayment, verifyPayment } from "../api/paymentsApi";

function CheckoutButton({ orderId, amount }) {
  const handlePayment = async () => {
    const res = await createPayment(orderId);
    const { razorpay_order_id } = res;

    const options = {
      key: process.env.REACT_APP_RAZORPAY_KEY_ID,
      amount: amount * 100,
      currency: "INR",
      name: "Sahil Footwear",
      description: "Order Payment",
      order_id: razorpay_order_id,
      handler: async function (response) {
        await verifyPayment({
          payment_id: razorpay_order_id,
          razorpay_payment_id: response.razorpay_payment_id,
          razorpay_signature: response.razorpay_signature,
        });
        alert("Payment Successful!");
      },
      theme: { color: "#3399cc" },
    };

    const rzp = new window.Razorpay(options);
    rzp.open();
  };

  return <button onClick={handlePayment}>Pay Now</button>;
}

export default CheckoutButton;