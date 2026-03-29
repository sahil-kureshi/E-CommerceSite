import api from "./axiosConfig";

// Signup
export const signup = async (userData) => {
  const response = await api.post("/signup", userData);
  return response.data;
};

// Login
export const login = async (credentials) => {
  const response = await api.post("/login", credentials);
  if (response.data.access_token) {
    localStorage.setItem("access_token", response.data.access_token);
  }
  return response.data;
};


// Get logged-in user's profile
export const getMyProfile = async () => {
  const response = await api.get("/customers/me");
  return response.data;
};

// Update profile
export const updateProfile = async (profileData) => {
  const response = await api.put("/customers/me", profileData);
  return response.data;
};