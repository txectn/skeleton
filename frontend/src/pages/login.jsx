// import { useState } from "react";
// import { useNavigate } from "react-router-dom";
// import { useSignIn, useSignUp } from "@clerk/clerk-react";

// export default function Login() {
//   const navigate = useNavigate();

//   const { isLoaded: signInLoaded, signIn } = useSignIn();
//   const { isLoaded: signUpLoaded, signUp } = useSignUp();

//   const [email, setEmail] = useState("");
//   const [loading, setLoading] = useState(false);

//   const handleLogin = async (e) => {
//     e.preventDefault();

//     if (!signInLoaded || !signUpLoaded) return;

//     try {
//       setLoading(true);

//       try {
//         // Existing user
//         await signIn.create({
//           strategy: "email_code",
//           identifier: email,
//         });

//         sessionStorage.setItem("authFlow", "signIn");
//       } catch (error) {
//         // User doesn't exist → create account
//         if (
//           error.errors?.[0]?.code === "form_identifier_not_found"
//         ) {
//           await signUp.create({
//             emailAddress: email,
//           });

//           await signUp.prepareEmailAddressVerification({
//             strategy: "email_code",
//           });

//           sessionStorage.setItem("authFlow", "signUp");
//         } else {
//           throw error;
//         }
//       }

//       navigate("/verify-otp");
//     } catch (err) {
//       console.log(err);
//     } finally {
//       setLoading(false);
//     }
//   };

//   return (
//     <form onSubmit={handleLogin}>
//       <input
//         type="email"
//         placeholder="Enter your email"
//         value={email}
//         onChange={(e) => setEmail(e.target.value)}
//       />

//       <button type="submit" disabled={loading}>
//         {loading ? "Sending..." : "Continue"}
//       </button>
//     </form>
//   );
// }








// import { useEffect, useState } from "react";
// import { useNavigate } from "react-router-dom";
// import {
//   useClerk,
//   useSignIn,
//   useSignUp,
// } from "@clerk/clerk-react";

// export default function Login() {
//   const navigate = useNavigate();

//   const { signOut } = useClerk();
//   const { isLoaded: signInLoaded, signIn } = useSignIn();
//   const { isLoaded: signUpLoaded, signUp } = useSignUp();

//   const [email, setEmail] = useState("");
//   const [loading, setLoading] = useState(false);

//   // Clear any existing Clerk session when this page opens
//   useEffect(() => {
//     const clearClerkSession = async () => {
//       try {
//         await signOut();
//       } catch (error) {
//         console.error(error);
//       }
//     };

//     clearClerkSession();
//   }, [signOut]);

//   const handleLogin = async (e) => {
//     e.preventDefault();

//     if (!signInLoaded || !signUpLoaded) return;

//     setLoading(true);

//     try {
//       let authFlow = "signIn";

//       try {
//         // Existing user
//         await signIn.create({
//           strategy: "email_code",
//           identifier: email,
//         });
//       } catch (error) {
//         // User doesn't exist → create account
//         if (error.errors?.[0]?.code !== "form_identifier_not_found") {
//           throw error;
//         }

//         authFlow = "signUp";

//         await signUp.create({
//           emailAddress: email,
//         });

//         await signUp.prepareEmailAddressVerification({
//           strategy: "email_code",
//         });
//       }

//       navigate("/verify-otp", {
//         state: {
//           email,
//           authFlow,
//         },
//       });
//     } catch (error) {
//       console.error(error);
//     } finally {
//       setLoading(false);
//     }
//   };

//   return (
//     <form onSubmit={handleLogin}>
//       <input
//         type="email"
//         placeholder="Enter your email"
//         value={email}
//         onChange={(e) => setEmail(e.target.value)}
//       />

//       <button type="submit" disabled={loading}>
//         {loading ? "Sending..." : "Continue"}
//       </button>
//     </form>
//   );
// }













import { useEffect, useState } from "react";
import { useClerk, useSignIn, useSignUp } from "@clerk/clerk-react";

export default function Login() {
  const { signOut } = useClerk();

  const { isLoaded: signInLoaded, signIn } = useSignIn();
  const { isLoaded: signUpLoaded, signUp } = useSignUp();

  const [email, setEmail] = useState("");
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const clearSession = async () => {
      try {
        // Remove previous flow
        sessionStorage.removeItem("authFlow");

        // Clear Clerk session
        await signOut();
      } catch (err) {
        console.error(err);
      }
    };

    clearSession();
  }, [signOut]);

  const handleLogin = async (e) => {
    e.preventDefault();

    if (!signInLoaded || !signUpLoaded || loading) return;

    setLoading(true);

    try {
      try {
        // Existing user
        await signIn.create({
          strategy: "email_code",
          identifier: email,
        });

        sessionStorage.setItem("authFlow", "signIn");
      } catch (err) {
        if (err.errors?.[0]?.code !== "form_identifier_not_found") {
          throw err;
        }

        // New user
        await signUp.create({
          emailAddress: email,
        });

        await signUp.prepareEmailAddressVerification({
          strategy: "email_code",
        });

        sessionStorage.setItem("authFlow", "signUp");
      }

      window.location.href = "/verify-otp";
    } catch (err) {
      console.error(err);

      alert(
        err.errors?.[0]?.longMessage ||
          err.message ||
          "Unable to send OTP."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleLogin}>
      <input
        type="email"
        placeholder="Enter your email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
      />

      <button type="submit" disabled={loading}>
        {loading ? "Sending..." : "Continue"}
      </button>
    </form>
  );
}