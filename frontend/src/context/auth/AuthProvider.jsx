import {
    createContext,
    useContext,
    useEffect,
    useMemo,
    useState,
} from "react";

import { useVerifyAuth } from "../../hooks/queries/authVerify";

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
    const { data, isPending, isError } = useVerifyAuth();

    const [authStatus, setAuthStatus] = useState("loading");

    useEffect(() => {
        if (isPending) return;

        if (isError || data === undefined) {
            setAuthStatus("unauthenticated");
            return;
        }

        setAuthStatus(
            data?.success === true
                ? "authenticated"
                : "unauthenticated"
        );
    }, [data, isPending, isError]);

    const login = () => {
        setAuthStatus("authenticated");
    };

    const logout = () => {
        setAuthStatus("unauthenticated");
    };

    const isAuthenticated = authStatus === "authenticated";

    const value = useMemo(
        () => ({
            authStatus,
            isAuthenticated,
            login,
            logout,
        }),
        [authStatus, isAuthenticated]
    );

    // Handle initial verification inside the provider.
    if (authStatus === "loading") {
        return null;
    }

    return (
        <AuthContext.Provider value={value}>
            {children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => {
    const context = useContext(AuthContext);

    if (!context) {
        throw new Error("useAuth must be used inside AuthProvider");
    }

    return context;
};
