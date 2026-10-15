import { Link as RouterLink } from "react-router-dom"
import * as React from "react";
import { useNavigate } from "react-router-dom";

import { ACCESS_TOKEN, REFRESH_TOKEN, DASHBOARD_ENDPOINT } from "../../../config";
import { useAuth } from "../../../context/auth/AuthProvider";

import Button from "@mui/material/Button";
import Menu from "@mui/material/Menu";
import MenuItem from "@mui/material/MenuItem";

import Divider from "@mui/material/Divider";

import { UserRound, LogOut } from "lucide-react";

import {
    iconsStyles,
    hoverStyles,
    menuBtnFont,
} from "../dashboardStyle";
import { css, padding } from "@mui/system";

export default function DashboardprofileAction() {
    const { logout } = useAuth();
    const navigate = useNavigate();

    const [anchorEl, setAnchorEl] = React.useState(null);
    const open = Boolean(anchorEl);

    const id = React.useId();
    const buttonId = `${id}-button`;
    const menuId = `${id}-menu`;

    const cssStyles = {
        hoverInverse: {
            backgroundColor: "transparent",
            color: iconsStyles.color_inverse,

            "&:hover": {
                backgroundColor: hoverStyles.mui_inverse,
            },

            "& .MuiTouchRipple-root": {
                color: hoverStyles.mui_ripple_inverse,
            },

            "& .MuiTouchRipple-child": {
                color: hoverStyles.mui_ripple_inverse,
            },
        },

        hoverMain: {
            backgroundColor: "transparent",
            color: iconsStyles.color_main,

            "&:hover": {
                backgroundColor: hoverStyles.mui_main,
            },

            "& .MuiTouchRipple-root": {
                color: hoverStyles.mui_ripple,
            },

            "& .MuiTouchRipple-child": {
                color: hoverStyles.mui_ripple,
            },
        },

        font: {
            ...menuBtnFont.alignMent,
            fontSize: menuBtnFont.size,
            fontSize: "var(--fs-sm)",
            fontWeight: menuBtnFont.weight,
            color: menuBtnFont.color_main,
        },

        menuItem: {
            paddingBottom: "1rem",
            paddingTop: "1rem",
            justifyContent: "flex-start",
            gap: "7px",
        }
    };

    console.log("access token:", localStorage.getItem(ACCESS_TOKEN));
    console.log("refresh token:", localStorage.getItem(REFRESH_TOKEN));

    const handleClick = (event) => {
        setAnchorEl(event.currentTarget);
    };

    const handleClose = () => {
        setAnchorEl(null);
    };

    const handleLogout = () => {
        // 1. Remove authentication tokens
        localStorage.removeItem(ACCESS_TOKEN);
        localStorage.removeItem(REFRESH_TOKEN);

        // 2. Update authentication context
        logout();

        // 3. Close the profile menu
        handleClose();

        // 4. Redirect to the home page
        navigate("/", { replace: true });
    };

    return (
        <div>
            <Button
                sx={{
                    ...cssStyles.hoverInverse,
                    border: "1px solid var(--border-inverse)",
                    padding: "0px",
                    minWidth: "45px",
                    minHeight: "45px",
                    width: "45px",
                    height: "45px",
                    borderRadius: "50%",
                }}
                id={buttonId}
                aria-controls={open ? menuId : undefined}
                aria-haspopup="true"
                aria-expanded={open}
                onClick={handleClick}
            >
                <UserRound
                    size={iconsStyles.size}
                    color={iconsStyles.color_inverse}
                />
            </Button>

            <Menu
                id={menuId}
                anchorEl={anchorEl}
                open={open}
                onClose={handleClose}
                slotProps={{
                    list: {
                        "aria-labelledby": buttonId,
                        sx: {
                            padding: "0px",
                        }
                    },
                }}
            >
                {/* <Divider sx={{
                    '&.MuiDivider-root': {
                        margin: "0px",
                    },
                }}
                /> */}
                <MenuItem
                    sx={{
                        ...cssStyles.font,
                        ...cssStyles.hoverMain,
                        ...cssStyles.menuItem,
                    }}
                    onClick={handleLogout}
                >
                    <span style={{
                        display: "flex",
                        alignItems: "center",
                    }}
                    >
                        <LogOut
                            size={17}
                            color={iconsStyles.color_main}
                        />
                    </span>
                    <span style={{
                        display: "flex",
                        alignItems: "center",
                    }}
                    >
                        Logout
                    </span>
                </MenuItem>
            </Menu>
        </div>
    );
}