import { useState } from "react";
import { Outlet, Link as RouterLink } from "react-router-dom";

import Link from "@mui/material/Link";
import IconButton from '@mui/material/IconButton';
import List from "@mui/material/List";
import Divider from '@mui/material/Divider';
import Drawer from '@mui/material/Drawer';

// lucide icons
import {
    Menu,
    UsersRound,
    PanelLeftOpen,
    PanelRightOpen,
    Tags,
    PackageCheck
} from "lucide-react";

// constant styles
import { iconsStyles, logoStyles } from "./dashboardStyle";

import { DASHBOARD_ENDPOINT } from '../../config'
import styles from "./dashboard.module.css"
import DashboardDropdown from "./dropdowns/dashboardDropdown";
import DashboardprofileAction from "./profile/profileAction";

export default function Dashboard() {
    const [open, setOpen] = useState(true);

    const [mobileOpen, setMobileOpen] = useState(false);
    const toggleDrawer = () => {
        setMobileOpen(!mobileOpen);
    }

    const navigationData = [
        {
            id: 1,
            name: 'Accounts',
            link: `${DASHBOARD_ENDPOINT}/accounts`,
            icon: UsersRound,
            child: [
                {
                    id: 1,
                    name: "Users",
                    link: `${DASHBOARD_ENDPOINT}/accounts/users`,
                    icon: null
                },
            ]
        },
        {
            id: 2,
            name: 'Products',
            link: `${DASHBOARD_ENDPOINT}/products`,
            icon: Tags,
            child: [
                {
                    id: 1,
                    name: 'Collection',
                    icon: null,
                    link: `${DASHBOARD_ENDPOINT}/collection`,
                },
                {
                    id: 2,
                    name: 'Inventory',
                    icon: null,
                    link: `${DASHBOARD_ENDPOINT}/inventory`,
                },
            ]
        },
        {
            id: 3,
            name: 'Orders',
            link: `${DASHBOARD_ENDPOINT}/orders`,
            icon: PackageCheck,
        },
    ];

    const drawerElements = (isopen, setMobileOpen, updateState) => {
        return (
            <>
                <div className={`${styles.drawerHeader}`}>
                    <Link
                        component={RouterLink}
                        to={DASHBOARD_ENDPOINT}
                        underline="none"
                        sx={{
                            transition: "opacity 0.2s ease-in-out",
                            "&:hover": { opacity: 0.8 },
                        }}
                        className={styles.logo}
                    >
                        Dashboard
                    </Link>
                    <IconButton
                        edge="start"
                        aria-label="close drawer"
                        sx={{
                            ml: 0,
                            borderRadius: "5px",
                            "&:hover": { backgroundColor: "transparent", },
                            "& .MuiTouchRipple-root": {
                                borderRadius: "5px",
                            },
                            "& .MuiTouchRipple-child": {
                                borderRadius: "5px",
                            },
                        }}
                        className={`${styles.drawerClose}`}
                        onClick={() => {
                            setOpen(false);
                            setMobileOpen(false);
                        }}
                    >
                        <PanelRightOpen size={iconsStyles.size} color={iconsStyles.color_inverse} />
                    </IconButton>
                </div>
                <Divider />
                <List sx={{ width: "100%", padding: 0 }}>
                    <DashboardDropdown data={navigationData} open={isopen} setOpen={setMobileOpen} updateState={updateState} />
                </List>
            </>
        )
    }

    return (
        <div className={styles.Layout}>
            <header className={`${styles.header} ${styles.transition} ${open ? styles.headerOpen : ""}`}>
                <nav className={styles.headerNav}>
                    <div className={`${styles.headerLeft} ${open ? styles.headerLeftOpen : ""}`}>
                        <IconButton
                            edge="start"
                            aria-label="menu"
                            sx={{
                                ml: 0,
                                mr: 1.7,
                                "&:hover": { backgroundColor: "transparent" },
                            }}
                            className={` ${styles.menuButtonDesktop} ${styles.menuButton}`}
                            onClick={() => setOpen(!open)}
                        >
                            <PanelLeftOpen size={iconsStyles.size} color={iconsStyles.color_inverse} />
                            <img src="/logoWhite.png" alt="logo" width={logoStyles.size} />
                        </IconButton>
                        <IconButton
                            edge="start"
                            aria-label="menu"
                            sx={{
                                ml: 0,
                                mr: 0.5,
                                width: "40px",
                                height: "40px",
                                padding: "8px",
                                "&:hover": { backgroundColor: "var(--bg-hover-mui-inverse)" },
                                '& .MuiTouchRipple-root': {
                                    color: "var(--bg-hover-mui-ripple-inverse)",
                                }
                            }}
                            className={`${styles.menuButtonMobile} ${styles.menuButton}`}
                            onClick={() => setMobileOpen(!mobileOpen)}
                        >
                            <Menu size={iconsStyles.size} color={iconsStyles.color_inverse} />
                        </IconButton>
                    </div>
                    <div className={`${styles.headerCenter} ${open ? styles.headerCenterOpen : ""}`}>
                        <Link
                            component={RouterLink}
                            to={DASHBOARD_ENDPOINT}
                            underline="none"
                            sx={{
                                transition: "opacity 0.2s ease-in-out",
                                "&:hover": { opacity: 0.8 },
                            }}
                            className={styles.logo}
                        >
                            <img className={styles.logo_image_mobile} src="/logoWhite.png" alt="logo" width={logoStyles.size} />
                            Dashboard
                        </Link>
                    </div>
                    <div className={styles.headerRight}>
                        <div className={styles.headerRightAction}>
                            <DashboardprofileAction />
                        </div>
                    </div>
                </nav>
            </header>
            <aside className={`${styles.drawer} ${styles.transition} ${open ? styles.drawerOpen : ""}`}>
                {drawerElements(open)}
            </aside>
            <Drawer
                className={styles.mobileDrawer}
                open={mobileOpen}
                onClose={toggleDrawer}
                anchor="left"
                sx={{
                    "& .MuiDrawer-paper": {
                        width: 260,
                        backgroundColor: "var(--bg-main)",
                    },
                }}
            >
                {drawerElements(mobileOpen, setMobileOpen, true)}
            </Drawer>
            <main className={`${styles.main}`}>
                <Outlet />
                <footer className={styles.footer}>© {new Date().getFullYear()} OGON. All rights reserved.</footer>
            </main>
        </div>
    )
}