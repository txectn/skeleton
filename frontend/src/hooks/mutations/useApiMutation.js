import { useMutation } from "@tanstack/react-query";
import { post, put, patch, remove } from "../../services/apiService/method";

const mutationMethods = {
    post,
    put,
    patch,
    delete: remove,
};

export const useApiMutation = ({
    method = "post",

    // ==========================================
    // API Options
    // ==========================================
    path,
    params,
    headers,
    auth = true,

    // ==========================================
    // TanStack Mutation Options
    // ==========================================
    ...mutationOptions
}) => {
    return useMutation({
        mutationFn: ({ body, params: mutationParams, headers: mutationHeaders } = {}) =>
            mutationMethods[method]({
                path,
                body,
                params: mutationParams ?? params,
                headers: mutationHeaders ?? headers,
                auth,
            }),

        ...mutationOptions,
    });
};