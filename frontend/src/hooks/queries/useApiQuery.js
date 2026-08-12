import { useQuery } from "@tanstack/react-query";
import { get } from "../../services/apiService/method";

export const useApiQuery = ({
    // ==========================================
    // API Options
    // ==========================================
    path,
    params,
    headers,
    auth = false,

    // ==========================================
    // TanStack Query Options
    // ==========================================
    queryKey,
    ...queryOptions
}) => {
    return useQuery({
        queryKey,

        queryFn: ({ signal }) =>
            get({
                path,
                params,
                headers,
                auth,
                signal,
            }),

        ...queryOptions,
    });
};