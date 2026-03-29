import api from "./axiosConfig";

// Get all products
export const getProducts = async () => {
  const response = await api.get("/products");
  return response.data;
};

// Get single product by ID
export const getProductById = async (productId) => {
  const response = await api.get(`/products/${productId}`);
  return response.data;
};

// Add new product (Admin only)
export const addProduct = async (productData) => {
  const response = await api.post("/products", productData);
  return response.data;
};