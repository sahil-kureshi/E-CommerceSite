import api from "./axiosConfig";

// Create payment order
export const createPayment = async (orderId) => {
  const response = await api.post("/create-payment", { order_id: orderId });
  return response.data;
};

// Verify payment
export const verifyPayment = async (paymentData) => {
  const response = await api.post("/verify-payment", paymentData);
  return response.data;
};