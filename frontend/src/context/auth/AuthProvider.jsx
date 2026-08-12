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
    const { data } = useVerifyAuth();

    const [isAuthenticated, setIsAuthenticated] = useState(false);

    useEffect(() => {
        if (data !== undefined) {
            setIsAuthenticated(data?.success);
        }
        console.log("succes: " + data?.success);
    }, [data]);

    const login = () => {
        setIsAuthenticated(true);
    };

    const logout = () => {
        setIsAuthenticated(false);
    };

    const value = useMemo(
        () => ({
            isAuthenticated,
            login,
            logout,
        }),
        [isAuthenticated]
    );

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