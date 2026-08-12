import { useAuth } from "./AuthProvider";

const RequireAuth = ({ children }) => {
    const { isAuthenticated } = useAuth();

    if (!isAuthenticated) {
        return null;
    }

    return children;
};

export default RequireAuth;