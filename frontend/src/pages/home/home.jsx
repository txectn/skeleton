// import { Link } from "react-router-dom"
// export default function Home() {
//     return (
//         <div>
//             <h1>Home</h1>
//             <Link to="/login">Login</Link>
//         </div>
//     )
// }

// import axios from "axios";
// import { Link } from "react-router-dom";
// import { GoogleLogin } from "@react-oauth/google";

// export default function Home() {
//     const handleGoogleSuccess = async (credentialResponse) => {
//         try {
//             const idToken = credentialResponse.credential;

//             const response = await axios.post(
//                 "http://127.0.0.1:8000/api/auth/",
//                 {
//                     provider: "google",
//                     device: {
//                         device: "Desktop",
//                         browser: navigator.userAgent,
//                         operating_system: navigator.platform,
//                     },
//                 },
//                 {
//                     headers: {
//                         Authorization: `Bearer ${idToken}`,
//                     },
//                 }
//             );

//             const { tokens } = response.data;

//             localStorage.setItem("access", tokens.access);
//             localStorage.setItem("refresh", tokens.refresh);

//             console.log("Logged in successfully.");
//         } catch (error) {
//             console.error(error);
//         }
//     };

//     const handleGoogleError = () => {
//         console.error("Google login failed.");
//     };

//     return (
//         <div>
//             <h1>Home</h1>

//             <Link to="/login">Login</Link>

//             <br />
//             <br />

//             <GoogleLogin
//                 onSuccess={handleGoogleSuccess}
//                 onError={handleGoogleError}
//                 useOneTap={false}
//             />
//         </div>
//     );
// }




// import { useState } from "react";
// import axios from "axios";
// import { Link } from "react-router-dom";
// import { GoogleLogin } from "@react-oauth/google";

// export default function Home() {
//     const [responseData, setResponseData] = useState(null);

//     const handleGoogleSuccess = async (credentialResponse) => {
//         try {
//             const idToken = credentialResponse.credential;

//             const response = await axios.post(
//                 "http://127.0.0.1:8000/api/auth/",
//                 {
//                     provider: "google",
//                     device: {
//                         device: "Desktop",
//                         browser: navigator.userAgent,
//                         operating_system: navigator.platform,
//                     },
//                 },
//                 {
//                     headers: {
//                         Authorization: `Bearer ${idToken}`,
//                     },
//                 }
//             );

//             // Show backend response
//             setResponseData(response.data);

//             console.log(response.data);
//         } catch (error) {
//             if (error.response) {
//                 setResponseData(error.response.data);
//             } else {
//                 setResponseData({
//                     error: error.message,
//                 });
//             }

//             console.error(error);
//         }
//     };

//     const handleGoogleError = () => {
//         setResponseData({
//             error: "Google login failed.",
//         });
//     };

//     return (
//         <div>
//             <h1>Home</h1>

//             <Link to="/login">Login</Link>

//             <br />
//             <br />

//             <GoogleLogin
//                 onSuccess={handleGoogleSuccess}
//                 onError={handleGoogleError}

//                 theme="outline"          // outline | filled_blue | filled_black
//                 size="large"             // small | medium | large
//                 text="continue_with"     // signin_with | signup_with | continue_with | signin
//                 shape="rectangular"      // rectangular | pill | circle | square
//                 logo_alignment="left"    // left | center
//                 width="320"
//                 locale="en"
//             />

//             <h1>Response</h1>

//             <h1>
//                 <pre>
//                     {responseData
//                         ? JSON.stringify(responseData, null, 4)
//                         : "No response yet."}
//                 </pre>
//             </h1>
//         </div>
//     );
// }















// import { Link } from "react-router-dom";
// import { GOOGLE_CLIENT_ID } from "../../config";
// // const GOOGLE_CLIENT_ID = import.meta.env.VITE_GOOGLE_CLIENT_ID;

// // const REDIRECT_URI = "http://localhost:5173/auth/google/callback";
// const REDIRECT_URI = "https://carport-skedaddle-spoiled.ngrok-free.dev/auth/google/callback";

// export default function Home() {
//     const handleGoogleLogin = () => {
//         const params = new URLSearchParams({
//             client_id: GOOGLE_CLIENT_ID,
//             redirect_uri: REDIRECT_URI,
//             response_type: "code",
//             scope: "openid email profile",
//             access_type: "offline",
//             prompt: "select_account",
//         });

//         window.location.href =
//             `https://accounts.google.com/o/oauth2/v2/auth?${params.toString()}`;
//     };

//     return (
//         <div>
//             <h1>Home</h1>

//             <Link to="/login">
//                 Login
//             </Link>

//             <br />
//             <br />

//             <button onClick={handleGoogleLogin}>
//                 Continue with Google
//             </button>
//         </div>
//     );
// }


import { Link } from "react-router-dom";
import { useState, useEffect, useRef } from "react";
import {
    GOOGLE_CLIENT_ID,
    FACEBOOK_APP_ID,
    GOOGLE_REDIRECT_URI,
    FACEBOOK_REDIRECT_URI
} from "../../config";
import { useApiQuery } from "../../hooks/queries/useApiQuery";
import { useApiMutation } from "../../hooks/mutations/useApiMutation";
import { useIsFetching } from "@tanstack/react-query";
import { useQueryClient } from "@tanstack/react-query";
import RequireAuth from "../../context/auth/RequireAuth";

import { useAuth } from "../../context/auth/AuthProvider";

export default function Home() {

    const { logout } = useAuth();

    const [id, setId] = useState(1);

    const queryClient = useQueryClient();

    const { data: profile, isLoading, error, refetch } = useApiQuery({
        path: "/api/profile",
        auth: true,
        params: {
            q: "",
        },
        queryKey: ["profile", id],
    });


    // Logout All
    const {
        mutate: logoutAll,
        data: logoutAllData,
        isPending: logoutAllIsLoading,
        error: logoutAllError,
    } = useApiMutation({
        path: "/api/logout-all/",
        auth: true,
        onSuccess: () => {
            queryClient.removeQueries({
                queryKey: ["profile"],
            });
        },
    });

    console.log(profile);

    useEffect(() => {
        console.log(JSON.stringify(logoutAllData, null, 2));
        if (logoutAllData?.success === true) logout();
    }, [logoutAllData]);

    const handleRefetch = () => {
        refetch();
        setId(id + 1);
    };

    // if (isFetching) {
    //     return <h1>Loading...</h1>;
    // }



    const isFetching = useIsFetching();

    const [showLoader, setShowLoader] = useState(true);

    const loadingStartedAt = useRef(null);
    const hasLoadedOnce = useRef(false);

    useEffect(() => {
        // Initial load is already finished.
        // Ignore all future fetches.
        if (hasLoadedOnce.current) {
            return;
        }

        let timer;

        if (isFetching > 0) {
            if (!loadingStartedAt.current) {
                loadingStartedAt.current = Date.now();
            }

            setShowLoader(true);
        } else {
            const elapsed = Date.now() - (loadingStartedAt.current ?? Date.now());
            const remaining = Math.max(1000 - elapsed, 0);

            timer = setTimeout(() => {
                hasLoadedOnce.current = true;
                setShowLoader(false);
                loadingStartedAt.current = null;
            }, remaining);
        }

        return () => clearTimeout(timer);
    }, [isFetching]);

    if (showLoader) {
        return <h1>Loading...</h1>;
    }


    const handleGoogleLogin = () => {
        const params = new URLSearchParams({
            client_id: GOOGLE_CLIENT_ID,
            redirect_uri: GOOGLE_REDIRECT_URI,
            response_type: "code",
            scope: "openid email profile",
            access_type: "offline",
            prompt: "select_account",
        });

        window.location.href =
            `https://accounts.google.com/o/oauth2/v2/auth?${params.toString()}`;
    };

    const handleFacebookLogin = () => {
        const params = new URLSearchParams({
            client_id: FACEBOOK_APP_ID,
            redirect_uri: FACEBOOK_REDIRECT_URI,
            response_type: "code",
            scope: "email,public_profile",
        });

        window.location.href =
            `https://www.facebook.com/v23.0/dialog/oauth?${params.toString()}`;
    };

    return (
        <div>
            <h1>Home without auth</h1>
            <RequireAuth><h1>Home with auth</h1></RequireAuth>
            <Link to="/login">
                Login
            </Link>

            <br />
            <br />

            <button onClick={handleGoogleLogin}>
                Continue with Google
            </button>

            <br />
            <br />

            <button onClick={handleFacebookLogin}>
                Continue with Facebook
            </button>
            {isLoading ? <h1>Loading...</h1> : <h1><pre>{JSON.stringify(profile, null, 2)}</pre></h1>}
            <button onClick={handleRefetch}>
                Refetch Profile
            </button>

            <button onClick={logoutAll}>
                Logout All
            </button>
        </div>
    );
}