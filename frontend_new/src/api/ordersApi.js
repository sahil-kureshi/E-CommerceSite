import api from "./axiosConfig";

// Create new order
export const createOrder = async (orderData) => {
  const response = await api.post("/orders", orderData);
  return response.data;
};

// Get orders for logged-in customer
export const getMyOrders = async () => {
  const response = await api.get("/orders/me");
  return response.data;
};