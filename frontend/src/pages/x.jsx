// import { useApiMutation } from "../hooks/mutations/useApiMutation";

// const CartTest = () => {
//     const addCartItemMutation = useApiMutation({
//         method: "post",
//         path: "/api/cart/",
//         auth: false,
//     });

//     const handleAddToCart = () => {
//         addCartItemMutation.mutate({
//             body: {
//                 variant: 4,
//                 quantity: 1,
//             },
//             headers: {
//                 Cookie: "cart_token=1c07d053-05d4-4a5b-b7be-54ed78445fc2",
//             },
//         });
//     };

//     return (
//         <div>
//             <button
//                 onClick={handleAddToCart}
//                 disabled={addCartItemMutation.isPending}
//             >
//                 {addCartItemMutation.isPending
//                     ? "Adding..."
//                     : "Add Variant 4"}
//             </button>

//                 <h1>
//                                 <pre>
//                 {addCartItemMutation.data
//                     ? JSON.stringify(addCartItemMutation.data, null, 2)
//                     : "No response yet"}
//             </pre>
//                 </h1>

//             {addCartItemMutation.error && (
//                 <pre>
//                     {JSON.stringify(
//                         addCartItemMutation.error,
//                         null,
//                         2
//                     )}
//                 </pre>
//             )}
//         </div>
//     );
// };

// export default CartTest;









// import { useState } from "react";
// import axios from "axios";

// const CartTest = () => {
//     const [customToken, setCustomToken] = useState("");
//     const [response, setResponse] = useState(null);
//     const [error, setError] = useState(null);

//     const setTestCookie = () => {
//         if (!customToken.trim()) {
//             setError({
//                 message: "Please enter a cart token.",
//             });

//             return;
//         }

//         document.cookie = `cart_token=${customToken.trim()}; path=/`;

//         setError(null);

//         console.log("Test cookie set:", customToken.trim());
//         console.log("document.cookie:", document.cookie);
//     };

//     const handleAddToCart = async () => {
//         setResponse(null);
//         setError(null);

//         try {
//             console.log("document.cookie:", document.cookie);

//             const result = await axios.post(
//                 "http://127.0.0.1:8000/api/cart/",
//                 {
//                     variant: 4,
//                     quantity: 1,
//                 },
//                 {
//                     withCredentials: true,
//                 }
//             );

//             console.log("Cart response:", result.data);

//             setResponse(result.data);
//         } catch (err) {
//             console.error("Cart request failed:", err);

//             setError({
//                 message: err.message,
//                 response: err.response?.data ?? null,
//                 status: err.response?.status ?? null,
//             });
//         }
//     };

//     return (
//         <div>
//             <h2>Cart Test</h2>

//             <div>
//                 <label>
//                     Custom Cart Token:
//                 </label>

//                 <br />

//                 <input
//                     type="text"
//                     value={customToken}
//                     onChange={(e) => setCustomToken(e.target.value)}
//                     placeholder="Enter cart token"
//                     style={{
//                         width: "400px",
//                         padding: "8px",
//                     }}
//                 />
//             </div>

//             <br />

//             <button onClick={setTestCookie}>
//                 Set Test Cookie
//             </button>

//             <button
//                 onClick={handleAddToCart}
//                 style={{
//                     marginLeft: "10px",
//                 }}
//             >
//                 Add Variant 4
//             </button>

//             <h3>Browser Cookie</h3>

//             <pre>
//                 {document.cookie || "No JavaScript-accessible cookies"}
//             </pre>

//             <h3>Response</h3>

//            <h1>
//              <pre>
//                 {response
//                     ? JSON.stringify(response, null, 2)
//                     : "No response yet"}
//             </pre>
//            </h1>

//             {error && (
//                 <>
//                     <h3>Error</h3>

//                     <h1>
//                         <pre>
//                         {JSON.stringify(error, null, 2)}
//                     </pre>
//                     </h1>
//                 </>
//             )}
//         </div>
//     );
// };

// export default CartTest;




import { useState } from "react";
import axios from "axios";

const CART_COOKIE = "cart_token";

const CartTest = () => {
    const [customToken, setCustomToken] = useState("");
    const [response, setResponse] = useState(null);
    const [error, setError] = useState(null);

    // ---------------------------------------------------------
    // Get cart_token only
    // ---------------------------------------------------------
    const getCartToken = () => {
        const cookies = document.cookie.split("; ");

        const cartCookie = cookies.find(
            (cookie) =>
                cookie.startsWith(`${CART_COOKIE}=`)
        );

        return cartCookie
            ? decodeURIComponent(
                  cartCookie.substring(
                      CART_COOKIE.length + 1
                  )
              )
            : null;
    };

    // ---------------------------------------------------------
    // Set custom test cookie
    // ---------------------------------------------------------
    const setTestCookie = () => {
        const token = customToken.trim();

        if (!token) {
            setError({
                message: "Please enter a cart token.",
            });

            return;
        }

        document.cookie = [
            `${CART_COOKIE}=${encodeURIComponent(token)}`,
            "path=/",
        ].join("; ");

        setError(null);

        console.log("cart_token:", token);
    };

    // ---------------------------------------------------------
    // Clear browser-accessible test cookie
    // ---------------------------------------------------------
    const clearTestCookie = () => {
        document.cookie = [
            `${CART_COOKIE}=`,
            "path=/",
            "expires=Thu, 01 Jan 1970 00:00:00 GMT",
        ].join("; ");

        setCustomToken("");
        setError(null);

        console.log("cart_token cleared");
    };

    // ---------------------------------------------------------
    // Add item
    // ---------------------------------------------------------
    const handleAddToCart = async () => {
        setResponse(null);
        setError(null);

        try {
            const cartToken = getCartToken();

            console.log(
                "cart_token:",
                cartToken ?? "HttpOnly / not JavaScript-accessible"
            );

            const result = await axios.post(
                "http://127.0.0.1:8000/api/cart/",
                {
                    variant: 4,
                    quantity: 1,
                },
                {
                    withCredentials: true,
                }
            );

            console.log("Cart response:", result.data);

            setResponse(result.data);
        } catch (err) {
            console.error(
                "Cart request failed:",
                err
            );

            setError({
                message: err.message,
                response: err.response?.data ?? null,
                status: err.response?.status ?? null,
            });
        }
    };

    return (
        <div>
            <h2>Cart Test</h2>

            <div>
                <label>
                    Custom Cart Token:
                </label>

                <br />

                <input
                    type="text"
                    value={customToken}
                    onChange={(e) =>
                        setCustomToken(e.target.value)
                    }
                    placeholder="Enter cart token"
                    style={{
                        width: "400px",
                        padding: "8px",
                    }}
                />
            </div>

            <br />

            <button onClick={setTestCookie}>
                Set Custom Cookie
            </button>

            <button
                onClick={clearTestCookie}
                style={{
                    marginLeft: "10px",
                }}
            >
                Clear Custom Cookie
            </button>

            <button
                onClick={handleAddToCart}
                style={{
                    marginLeft: "10px",
                }}
            >
                Add Variant 4
            </button>

            <h3>Cart Token</h3>

            <pre>
                {getCartToken() ||
                    "HttpOnly / not JavaScript-accessible"}
            </pre>

            <h3>Response</h3>

            <h1>
                <pre>
                {response
                    ? JSON.stringify(
                          response,
                          null,
                          2
                      )
                    : "No response yet"}
            </pre>
            </h1>

            {error && (
                <>
                    <h3>Error</h3>

                    <h1>
                                            <pre>
                        {JSON.stringify(
                            error,
                            null,
                            2
                        )}
                    </pre>
                    </h1>
                </>
            )}
        </div>
    );
};

export default CartTest;