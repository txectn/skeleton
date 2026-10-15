import { useState, useEffect, useRef } from "react";
import { useApiQuery } from "../../../hooks/queries/useApiQuery";

import Skeleton from '@mui/material/Skeleton';

import styles from "./accounts.module.css"

export default function Accounts() {
    const loadingStartTime = useRef(null);

    const [showLoading, setShowLoading] = useState(true);

    const [summaryId, setSummaryId] = useState(1);

    const { data: accountsSummary, isLoading, error, refetch } = useApiQuery({
        path: "/api/account-summary/",
        auth: true,
        params: {
            q: "",
        },
        queryKey: ["accountsSummary", summaryId],
    });

    useEffect(() => {
        if (isLoading) {
            loadingStartTime.current = Date.now();
            setShowLoading(true);
            return;
        }

        const elapsedTime = Date.now() - loadingStartTime.current;
        const remainingTime = Math.max(0, 1000 - elapsedTime);

        const timer = setTimeout(() => {
            setShowLoading(false);
            loadingStartTime.current = null;
        }, remainingTime);

        return () => clearTimeout(timer);
    }, [isLoading]);

    return (
        <div className={`${styles.container}`}>
            {/* {true ?
                <Skeleton
                    sx={{
                        backgroundColor: "var(--bg-skeleton-main)",
                        borderRadius: "5px",
                    }}
                    variant="rectangular"
                    animation="wave"
                    width={210}
                    height={118}
                />
                :
                <div>
                    <h1>Accounts</h1>
                </div>
            } */}
        </div>
    )
}