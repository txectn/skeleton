
import { Link as RouterLink } from "react-router-dom";

import Breadcrumbs from "@mui/material/Breadcrumbs";
import Typography from "@mui/material/Typography";
import Link from "@mui/material/Link";

const linkStyle = {
    display: "inline-block",
    fontSize: "var(--fs-sm-md)",
    fontWeight: "var(--fw-medium)",
    color: "var(--text-main)",
    opacity: 1,

    "&:hover": {
        opacity: 0.8,
    },
};

const currentStyle = {
    color: "var(--text-main)",
    fontSize: "var(--fs-sm-md)",
    fontWeight: "var(--fw-medium)",
    opacity: 0.6,
};

const breadCrumbStyle = {
    "& .MuiBreadcrumbs-separator": {
        color: "var(--text-main)",
        fontSize: "var(--fs-sm-md)",
        fontWeight: "var(--fw-medium)",
    },
}

export default function BreadcrumbsComponent({ data = [] }) {
    return (
        <Breadcrumbs
            separator="›"
            aria-label="breadcrumb"
            sx={breadCrumbStyle}
        >
            {data.map((item, index) =>
                item.current ? (
                    <Typography key={index} sx={currentStyle}>
                        {item.name}
                    </Typography>
                ) : (
                    <Link
                        key={index}
                        component={RouterLink}
                        to={item.link}
                        underline="none"
                        className={`underline`}
                        sx={linkStyle}
                    >
                        {item.name}
                    </Link>
                )
            )}
        </Breadcrumbs>
    );
}
