import axios from "axios";

// Create an Axios instance
export const api = axios.create({
  baseURL: "http://127.0.0.1:8000", // your FastAPI backend URL
});

// Add a request interceptor to include the token automatically
api.interceptors.request.use(
  (config) => {
    // Get the token from localStorage
    const token = localStorage.getItem("access_token");

    if (token && config.headers) {
      config.headers["Authorization"] = `Bearer ${token}`;
    }

    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);