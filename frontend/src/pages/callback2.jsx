import { useEffect, useState } from "react";
import axios from "axios";

export default function FacebookCallback() {
    const [responseData, setResponseData] = useState(
        "Completing Facebook login..."
    );

    useEffect(() => {
        const authenticate = async () => {
            try {
                const params = new URLSearchParams(
                    window.location.search
                );

                const code = params.get("code");

                if (!code) {
                    setResponseData(
                        "Facebook authorization code missing."
                    );
                    return;
                }

                const response = await axios.post(
                    "http://127.0.0.1:8000/api/auth/",
                    {
                        provider: "facebook",
                        device: {
                            device: "Desktop",
                            browser: navigator.userAgent,
                            operating_system: navigator.platform,
                        },
                    },
                    {
                        headers: {
                            Authorization: `Bearer ${code}`,
                        },
                    }
                );

                console.log("Backend response:", response.data);

                setResponseData(
                    JSON.stringify(response.data, null, 4)
                );

            } catch (error) {
                console.error(error);

                if (error.response) {
                    setResponseData(
                        JSON.stringify(
                            error.response.data,
                            null,
                            4
                        )
                    );
                } else {
                    setResponseData(error.message);
                }
            }
        };

        authenticate();

    }, []);

    return (
        <div>
            <h1>
                Facebook Callback
            </h1>

            <h1>
                <pre>
                    {responseData}
                </pre>
            </h1>
        </div>
    );
}