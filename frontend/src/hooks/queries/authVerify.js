import { useApiQuery } from "./useApiQuery";

export const useVerifyAuth = () => {
    return useApiQuery({
        path: "/api/auth/verify/",
        auth: true,

        queryKey: ["auth", "verify"],

        // select: (data) => data?.success === true,

        retry: false,
        refetchOnWindowFocus: false,
        refetchOnReconnect: true,
        refetchOnMount: true,
        staleTime: 0,
    });
};