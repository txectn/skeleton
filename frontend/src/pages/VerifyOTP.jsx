// import { useState } from "react";
// import { useNavigate } from "react-router-dom";
// import { useAuth, useSignIn, useSignUp } from "@clerk/clerk-react";

// export default function VerifyOTP() {
//   const navigate = useNavigate();

//   const { getToken } = useAuth();

//   const {
//     isLoaded: signInLoaded,
//     signIn,
//     setActive: setSignInActive,
//   } = useSignIn();

//   const {
//     isLoaded: signUpLoaded,
//     signUp,
//     setActive: setSignUpActive,
//   } = useSignUp();

//   const [code, setCode] = useState("");
//   const [loading, setLoading] = useState(false);
//   const [verified, setVerified] = useState(false);

//   const handleVerify = async (e) => {
//     e.preventDefault();

//     if (!signInLoaded || !signUpLoaded || loading || verified) {
//       return;
//     }

//     try {
//       setLoading(true);

//       const flow = sessionStorage.getItem("authFlow");

//       if (!flow) {
//         throw new Error("Authentication flow not found.");
//       }

//       let result;

//       if (flow === "signIn") {
//         result = await signIn.attemptFirstFactor({
//           strategy: "email_code",
//           code,
//         });

//         if (result.status === "complete") {
//           await setSignInActive({
//             session: result.createdSessionId,
//           });
//         }
//       } else if (flow === "signUp") {
//         result = await signUp.attemptEmailAddressVerification({
//           code,
//         });

//         if (result.status === "complete") {
//           await setSignUpActive({
//             session: result.createdSessionId,
//           });
//         }
//       } else {
//         throw new Error("Invalid authentication flow.");
//       }

//       if (result.status !== "complete") {
//         console.log("Verification incomplete:", result);
//         setLoading(false);
//         return;
//       }

//       const token = await getToken();

//       console.log("JWT Token:", token);

//       sessionStorage.removeItem("authFlow");

//       setVerified(true);
//       setLoading(false);

//       // Send JWT to your backend
//       // await axios.post("/api/auth/clerk/", {}, {
//       //   headers: {
//       //     Authorization: `Bearer ${token}`,
//       //   },
//       // });

//       // navigate("/");
//     } catch (err) {
//       console.error(err);

//       alert(
//         err.errors?.[0]?.longMessage ||
//           err.message ||
//           "OTP verification failed."
//       );

//       setLoading(false);
//     }
//   };

//   return (
//     <form onSubmit={handleVerify}>
//       <input
//         type="text"
//         placeholder="Enter OTP"
//         value={code}
//         onChange={(e) => setCode(e.target.value)}
//         disabled={loading || verified}
//       />

//       <button
//         type="submit"
//         disabled={loading || verified}
//       >
//         {verified
//           ? "Verified"
//           : loading
//           ? "Verifying..."
//           : "Verify OTP"}
//       </button>
//     </form>
//   );
// }




// import { useState } from "react";
// import { useNavigate } from "react-router-dom";
// import { useAuth, useSignIn, useSignUp } from "@clerk/clerk-react";

// export default function VerifyOTP() {
//   const navigate = useNavigate();

//   const { getToken } = useAuth();

//   const {
//     isLoaded: signInLoaded,
//     signIn,
//     setActive: setSignInActive,
//   } = useSignIn();

//   const {
//     isLoaded: signUpLoaded,
//     signUp,
//     setActive: setSignUpActive,
//   } = useSignUp();

//   const [code, setCode] = useState("");
//   const [loading, setLoading] = useState(false);
//   const [verified, setVerified] = useState(false);

//   const handleVerify = async (e) => {
//     e.preventDefault();

//     if (!signInLoaded || !signUpLoaded || loading || verified) {
//       return;
//     }

//     const flow = sessionStorage.getItem("authFlow");

//     if (!flow) {
//       alert("Authentication session expired.");
//       navigate("/login");
//       return;
//     }

//     try {
//       setLoading(true);

//       let result;

//       if (flow === "signIn") {
//         result = await signIn.attemptFirstFactor({
//           strategy: "email_code",
//           code,
//         });

//         if (result.status === "complete") {
//           await setSignInActive({
//             session: result.createdSessionId,
//           });
//         }
//       } else {
//         result = await signUp.attemptEmailAddressVerification({
//           code,
//         });

//         if (result.status === "complete") {
//           await setSignUpActive({
//             session: result.createdSessionId,
//           });
//         }
//       }

//       if (result.status !== "complete") {
//         console.log(result);
//         return;
//       }

//       const token = await getToken();

//       console.log(token);

//       sessionStorage.removeItem("authFlow");

//       setVerified(true);

//       // await axios.post("/api/auth/login/", {}, {
//       //   headers: {
//       //     Authorization: `Bearer ${token}`,
//       //   },
//       // });

//       // navigate("/");
//     } catch (err) {
//       console.error(err);

//       alert(
//         err.errors?.[0]?.longMessage ||
//           err.message ||
//           "OTP verification failed."
//       );
//     } finally {
//       setLoading(false);
//     }
//   };

//   return (
//     <form onSubmit={handleVerify}>
//       <input
//         type="text"
//         placeholder="Enter OTP"
//         value={code}
//         onChange={(e) => setCode(e.target.value)}
//         disabled={loading || verified}
//       />

//       <button disabled={loading || verified}>
//         {verified
//           ? "Verified"
//           : loading
//           ? "Verifying..."
//           : "Verify OTP"}
//       </button>
//     </form>
//   );
// }








// import { useState } from "react";
// import { useNavigate } from "react-router-dom";
// import { useAuth, useSignIn, useSignUp } from "@clerk/clerk-react";

// export default function VerifyOTP() {
//   const navigate = useNavigate();

//   const { getToken } = useAuth();

//   const {
//     isLoaded: signInLoaded,
//     signIn,
//     setActive: setSignInActive,
//   } = useSignIn();

//   const {
//     isLoaded: signUpLoaded,
//     signUp,
//     setActive: setSignUpActive,
//   } = useSignUp();

//   const [code, setCode] = useState("");
//   const [loading, setLoading] = useState(false);
//   const [verified, setVerified] = useState(false);
//   const [token, setToken] = useState("");

//   const handleVerify = async (e) => {
//     e.preventDefault();

//     if (!signInLoaded || !signUpLoaded || loading || verified) {
//       return;
//     }

//     const flow = sessionStorage.getItem("authFlow");

//     if (!flow) {
//       alert("Authentication session expired.");
//       navigate("/login");
//       return;
//     }

//     try {
//       setLoading(true);

//       let result;

//       if (flow === "signIn") {
//         result = await signIn.attemptFirstFactor({
//           strategy: "email_code",
//           code,
//         });

//         if (result.status === "complete") {
//           await setSignInActive({
//             session: result.createdSessionId,
//           });
//         }
//       } else {
//         result = await signUp.attemptEmailAddressVerification({
//           code,
//         });

//         if (result.status === "complete") {
//           await setSignUpActive({
//             session: result.createdSessionId,
//           });
//         }
//       }

//       if (result.status !== "complete") {
//         console.log(result);
//         return;
//       }

//       const jwtToken = await getToken();

//       setToken(jwtToken);

//       sessionStorage.removeItem("authFlow");

//       setVerified(true);

//       // await axios.post("/api/auth/login/", {}, {
//       //   headers: {
//       //     Authorization: `Bearer ${jwtToken}`,
//       //   },
//       // });

//       // navigate("/");
//     } catch (err) {
//       console.error(err);

//       alert(
//         err.errors?.[0]?.longMessage ||
//           err.message ||
//           "OTP verification failed."
//       );
//     } finally {
//       setLoading(false);
//     }
//   };

//   return (
//     <>
//       {token && <h1>{token}</h1>}

//       <form onSubmit={handleVerify}>
//         <input
//           type="text"
//           placeholder="Enter OTP"
//           value={code}
//           onChange={(e) => setCode(e.target.value)}
//           disabled={loading || verified}
//         />

//         <button disabled={loading || verified}>
//           {verified
//             ? "Verified"
//             : loading
//             ? "Verifying..."
//             : "Verify OTP"}
//         </button>
//       </form>
//     </>
//   );
// }









import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth, useSignIn, useSignUp } from "@clerk/clerk-react";
import axios from "axios";

export default function VerifyOTP() {
  const navigate = useNavigate();

  const { getToken } = useAuth();

  const {
    isLoaded: signInLoaded,
    signIn,
    setActive: setSignInActive,
  } = useSignIn();

  const {
    isLoaded: signUpLoaded,
    signUp,
    setActive: setSignUpActive,
  } = useSignUp();

  const [code, setCode] = useState("");
  const [loading, setLoading] = useState(false);
  const [verified, setVerified] = useState(false);
  const [response, setResponse] = useState(null);

  const handleVerify = async (e) => {
    e.preventDefault();

    if (!signInLoaded || !signUpLoaded || loading || verified) {
      return;
    }

    const flow = sessionStorage.getItem("authFlow");

    if (!flow) {
      alert("Authentication session expired.");
      navigate("/login");
      return;
    }

    try {
      setLoading(true);

      let result;

      if (flow === "signIn") {
        result = await signIn.attemptFirstFactor({
          strategy: "email_code",
          code,
        });

        if (result.status === "complete") {
          await setSignInActive({
            session: result.createdSessionId,
          });
        }
      } else {
        result = await signUp.attemptEmailAddressVerification({
          code,
        });

        if (result.status === "complete") {
          await setSignUpActive({
            session: result.createdSessionId,
          });
        }
      }

      if (result.status !== "complete") {
        console.log(result);
        return;
      }

      const clerkToken = await getToken();

      const deviceData = {
        device: navigator.platform || "Unknown Device",
        browser: navigator.userAgent,
        operating_system: navigator.userAgent,
      };

      const apiResponse = await axios.post(
        "http://127.0.0.1:8000/api/auth/",
        {
          provider: "clerk",
          device: deviceData,
        },
        {
          headers: {
            Authorization: `Bearer ${clerkToken}`,
            "Content-Type": "application/json",
          },
        }
      );

      setResponse(apiResponse.data);

      sessionStorage.removeItem("authFlow");

      setVerified(true);

      // navigate("/");
    } catch (err) {
      console.error(err);

      setResponse(err.response?.data || err.message);

      alert(
        err.response?.data?.detail ||
          err.errors?.[0]?.longMessage ||
          err.message ||
          "OTP verification failed."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      {response && (
        <h1>
          <pre>{JSON.stringify(response, null, 2)}</pre>
        </h1>
      )}

      <form onSubmit={handleVerify}>
        <input
          type="text"
          placeholder="Enter OTP"
          value={code}
          onChange={(e) => setCode(e.target.value)}
          disabled={loading || verified}
        />

        <button disabled={loading || verified}>
          {verified
            ? "Verified"
            : loading
            ? "Verifying..."
            : "Verify OTP"}
        </button>
      </form>
    </>
  );
}