import axios from "axios";
import { ACCESS_TOKEN, BASE_URL } from "../../config";
import { clearAuth, refreshToken } from "./refresh";

export const publicApi = axios.create({
    baseURL: BASE_URL,
    withCredentials: true
});

export const privateApi = axios.create({
    baseURL: BASE_URL,
    withCredentials: true
});

// Request Interceptor
privateApi.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem(ACCESS_TOKEN);

        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }

        return config;
    },
    (error) => Promise.reject(error)
);

// Response Interceptor
privateApi.interceptors.response.use(
    (response) => response,

    async (error) => {
        const originalRequest = error.config;

        // Network error
        if (!error.response) {
            return Promise.reject(error);
        }

        // Already retried once
        if (originalRequest._retry) {
            return Promise.reject(error);
        }

        // Access token expired
        if (error.response.status === 401) {
            originalRequest._retry = true;

            try {
                const accessToken = await refreshToken();

                originalRequest.headers.Authorization = `Bearer ${accessToken}`;

                return privateApi(originalRequest);
            } catch (err) {
                clearAuth();
                return Promise.reject(err);
            }
        }

        return Promise.reject(error);
    }
);