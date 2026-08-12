import { publicApi } from "./api";
import {
    ACCESS_TOKEN,
    REFRESH_TOKEN,
} from "../../config";

let refreshPromise = null;

export const refreshToken = async () => {
    // If a refresh is already in progress, wait for it.
    if (refreshPromise) {
        return refreshPromise;
    }

    refreshPromise = (async () => {
        try {
            const refreshToken = localStorage.getItem(REFRESH_TOKEN);

            if (!refreshToken) {
                throw new Error("Refresh token not found.");
            }

            const { data } = await publicApi.post("/api/refresh/", {
                refresh: refreshToken,
            });

            const accessToken = data.access;

            localStorage.setItem(ACCESS_TOKEN, accessToken);

            if (data.refresh) {
                localStorage.setItem(REFRESH_TOKEN, data.refresh);
            }

            return accessToken;
        } finally {
            refreshPromise = null;
        }
    })();

    return refreshPromise;
};

export const clearAuth = () => {
    localStorage.removeItem(ACCESS_TOKEN);
    localStorage.removeItem(REFRESH_TOKEN);
};