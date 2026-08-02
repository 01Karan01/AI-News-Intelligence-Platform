import axios from "axios";

const getApiBaseUrl = () => {
  const envUrl = import.meta.env.VITE_API_BASE_URL;

  if (envUrl) {
    console.log("[API] Using VITE_API_BASE_URL from environment:", envUrl);
    return envUrl;
  }

  const defaultUrl = "http://localhost:8000/api";
  console.log("[API] Using default API base URL:", defaultUrl);
  return defaultUrl;
};

export const BASE_URL = getApiBaseUrl();

const API = axios.create({
  baseURL: BASE_URL,
  timeout: 10000,
  headers: {
    "Content-Type": "application/json",
  },
});

API.interceptors.request.use(
  (config) => {
    const method = config.method?.toUpperCase() ?? "GET";
    console.log(`[API] ${method} ${config.baseURL}${config.url}`);
    return config;
  },
  (error) => {
    console.error("[API] Request configuration error:", error);
    return Promise.reject(error);
  },
);

API.interceptors.response.use(
  (response) => {
    const count = Array.isArray(response.data) ? response.data.length : "object";
    console.log(`[API] OK ${response.status} ${response.config.url} (${count})`);
    return response;
  },
  (error) => {
    if (error.response) {
      console.error(`[API] FAIL ${error.response.status} ${error.config?.url}`, {
        status: error.response.status,
        statusText: error.response.statusText,
        data: error.response.data,
      });
    } else if (error.request) {
      console.error(`[API] FAIL no response from ${error.config?.url}`, {
        message: error.message,
        code: error.code,
        url: error.config?.url,
      });
    } else {
      console.error("[API] FAIL request setup error:", error.message);
    }
    return Promise.reject(error);
  },
);

const validateResponse = (data, expectedType = "object") => {
  if (expectedType === "array" && !Array.isArray(data)) {
    throw new Error(`Expected array response, got ${typeof data}`);
  }

  if (expectedType === "object" && (typeof data !== "object" || data === null || Array.isArray(data))) {
    throw new Error(`Expected object response, got ${typeof data}`);
  }

  return data;
};

export const getEvents = async () => {
  const response = await API.get("/events");
  return validateResponse(response.data, "array");
};

export const getEventById = async (id) => {
  const response = await API.get(`/events/${id}`);
  return validateResponse(response.data, "object");
};

export const searchEvents = async (query = "") => {
  const response = await API.get("/events/search", { params: { q: query } });
  return validateResponse(response.data, "array");
};

export const getTimeline = async () => {
  const response = await API.get("/timeline");
  return validateResponse(response.data, "array");
};

export const getStatistics = async () => {
  const response = await API.get("/statistics");
  return validateResponse(response.data, "object");
};

export const checkHealth = async () => {
  const response = await API.get("/health");
  return validateResponse(response.data, "object");
};

export const getApiConfig = () => ({
  baseURL: API.defaults.baseURL,
  timeout: API.defaults.timeout,
  headers: API.defaults.headers,
});

export default API;
