// import * as React from 'react';
// import { Link } from "react-router-dom";
// import { styled, useTheme } from '@mui/material/styles';
// import Box from '@mui/material/Box';
// import MuiDrawer from '@mui/material/Drawer';
// import MuiAppBar from '@mui/material/AppBar';
// import Toolbar from '@mui/material/Toolbar';
// import List from '@mui/material/List';
// import Typography from '@mui/material/Typography';
// import CssBaseline from '@mui/material/CssBaseline';
// import Divider from '@mui/material/Divider';
// import IconButton from '@mui/material/IconButton';
// import MenuIcon from '@mui/icons-material/Menu';
// import ChevronLeftIcon from '@mui/icons-material/ChevronLeft';
// import ChevronRightIcon from '@mui/icons-material/ChevronRight';
// import ListItem from '@mui/material/ListItem';
// import ListItemButton from '@mui/material/ListItemButton';
// import ListItemIcon from '@mui/material/ListItemIcon';
// import ListItemText from '@mui/material/ListItemText';
// import PersonOutlinedIcon from '@mui/icons-material/PersonOutlined';
// import { Outlet } from 'react-router-dom';
// import { DASHBOARD_ENDPOINT } from '../../config';
// import styles from './dashboard.module.css'

// const listButtonIconStyles = {
//     width: 25,
//     height: 25,
//     color: 'inherit',
// };

// const listButtonTextStyles = {
//     fontSize: "var(--fs-base)",
//     color: "var(--text-main)",
// }

// const dashboardBrandStyles = {
//     fontSize: "var(--fs-xl)",
//     color: "var(--text-inverse)",
//     fontWeight: "var(--fw-semibold)",
//     textDecoration: "none",
//     transition: "opacity 0.2s ease-in-out",
//     "&:hover": {
//         opacity: 0.8,
//     },
// };

// const drawerWidth = 240;

// const openedMixin = (theme) => ({
//     width: drawerWidth,
//     transition: theme.transitions.create('width', {
//         easing: theme.transitions.easing.sharp,
//         duration: theme.transitions.duration.enteringScreen,
//     }),
//     overflowX: 'hidden',
// });

// const closedMixin = (theme) => ({
//     transition: theme.transitions.create('width', {
//         easing: theme.transitions.easing.sharp,
//         duration: theme.transitions.duration.leavingScreen,
//     }),
//     overflowX: 'hidden',
//     width: `calc(${theme.spacing(7)} + 1px)`,
//     [theme.breakpoints.up('sm')]: {
//         width: `calc(${theme.spacing(8)} + 1px)`,
//     },
// });

// const DrawerHeader = styled('div')(({ theme }) => ({
//     display: 'flex',
//     alignItems: 'center',
//     padding: theme.spacing(0, 1),
//     // necessary for content to be below app bar
//     ...theme.mixins.toolbar,
// }));

// const AppBar = styled(MuiAppBar, {
//     shouldForwardProp: (prop) => prop !== 'open',
// })(({ theme }) => ({
//     zIndex: theme.zIndex.drawer + 1,
//     transition: theme.transitions.create(['width', 'margin'], {
//         easing: theme.transitions.easing.sharp,
//         duration: theme.transitions.duration.leavingScreen,
//     }),
//     variants: [
//         {
//             props: ({ open }) => open,
//             style: {
//                 marginLeft: drawerWidth,
//                 width: `calc(100% - ${drawerWidth}px)`,
//                 transition: theme.transitions.create(['width', 'margin'], {
//                     easing: theme.transitions.easing.sharp,
//                     duration: theme.transitions.duration.enteringScreen,
//                 }),
//             },
//         },
//     ],
// }));

// const Drawer = styled(MuiDrawer, { shouldForwardProp: (prop) => prop !== 'open' })(
//     ({ theme }) => ({
//         width: drawerWidth,
//         flexShrink: 0,
//         whiteSpace: 'nowrap',
//         boxSizing: 'border-box',
//         '& .MuiDrawer-paper': {
//             borderRight: 0,
//         },
//         variants: [
//             {
//                 props: ({ open }) => open,
//                 style: {
//                     ...openedMixin(theme),
//                     '& .MuiDrawer-paper': openedMixin(theme),
//                 },
//             },
//             {
//                 props: ({ open }) => !open,
//                 style: {
//                     ...closedMixin(theme),
//                     '& .MuiDrawer-paper': closedMixin(theme),
//                 },
//             },
//         ],
//     }),
// );

// const DashboardBrand = ({ sx = {} }) => (
//     <Typography
//         component={Link}
//         to={DASHBOARD_ENDPOINT}
//         sx={[dashboardBrandStyles, sx]}
//     >
//         Dashboard
//     </Typography>
// );

// export default function Dashboard() {
//     const theme = useTheme();
//     const [open, setOpen] = React.useState(true);

//     const handleDrawerOpen = () => {
//         setOpen(true);
//     };

//     const handleDrawerClose = () => {
//         setOpen(false);
//     };

//     const drawerNavigationdata = [
//         {
//             id: 1,
//             name: "Accounts",
//             link: `${DASHBOARD_ENDPOINT}/accounts`,
//             icon: PersonOutlinedIcon
//         },
//     ];

//     return (
//         <Box sx={{ display: 'flex' }}>
//             <CssBaseline />
//             <AppBar
//                 sx={{
//                     backgroundColor: "var(--bg-inverse)",
//                 }}
//                 position="fixed" open={open}>
//                 <Toolbar sx={{ display: 'flex', justifyContent: 'space-between' }}>
//                     <Box sx={{ display: 'flex', alignItems: 'center' }}>
//                         <IconButton
//                             aria-label="open drawer"
//                             edge="start"
//                             onClick={handleDrawerOpen}
//                             sx={{
//                                 marginRight: 4,
//                                 ...(open && { display: 'none' }),
//                                 "&:hover": {
//                                     backgroundColor: "var(--bg-hover-mui-30)",
//                                 },
//                                 color: "var(--text-inverse)",
//                             }}
//                         >
//                             <MenuIcon sx={listButtonIconStyles} />
//                         </IconButton>
//                         <DashboardBrand sx={{ display: open ? "none" : "block" }} />
//                     </Box>
//                 </Toolbar>
//             </AppBar>
//             <Drawer variant="permanent" open={open}>
//                 <DrawerHeader
//                     sx={{
//                         justifyContent: 'space-between',
//                         backgroundColor: "var(--bg-inverse)",
//                     }}
//                 >
//                     <DashboardBrand
//                         sx={{
//                             display: open ? "block" : "none",
//                             paddingLeft: 1.5
//                         }}
//                     />
//                     <IconButton
//                         sx={{
//                             color: "var(--text-inverse)",
//                             display: open ? "block" : "none",
//                             "&:hover": {
//                                 backgroundColor: "var(--bg-hover-mui-30)",
//                             },
//                         }}
//                         aria-label="close drawer"
//                         onClick={handleDrawerClose
//                         }>
//                         {theme.direction === 'rtl' ? <ChevronRightIcon sx={listButtonIconStyles} /> : <ChevronLeftIcon sx={listButtonIconStyles} />}
//                     </IconButton>
//                 </DrawerHeader>
//                 <Divider />
//                 <List>
//                     {drawerNavigationdata.map((item) => (
//                         <ListItem key={item.id} disablePadding sx={{ display: 'block' }}>
//                             <ListItemButton
//                                 component={Link}
//                                 to={item.link}
//                                 sx={[
//                                     {
//                                         minHeight: 48,
//                                         px: 2.5,
//                                     },
//                                     open
//                                         ? {
//                                             justifyContent: 'initial',
//                                         }
//                                         : {
//                                             justifyContent: 'center',
//                                         },
//                                 ]}
//                             >
//                                 <ListItemIcon
//                                     sx={[
//                                         {
//                                             minWidth: 0,
//                                             justifyContent: 'center',
//                                         },
//                                         open
//                                             ? {
//                                                 mr: 3,
//                                             }
//                                             : {
//                                                 mr: 'auto',
//                                             },
//                                     ]}
//                                 >
//                                     {item.icon && <item.icon sx={listButtonIconStyles} />}
//                                 </ListItemIcon>
//                                 <ListItemText
//                                     primary={item.name}
//                                     slotProps={{
//                                         primary: {
//                                             sx: listButtonTextStyles,
//                                         },
//                                     }}
//                                     sx={[
//                                         open
//                                             ? { opacity: 1 }
//                                             : { opacity: 0 },
//                                     ]}
//                                 />
//                             </ListItemButton>
//                         </ListItem>
//                     ))}
//                 </List>
//             </Drawer>
//             <Box component="main" sx={{ flexGrow: 1, p: 3 }}>
//                 <DrawerHeader />
//                 <Outlet />
//             </Box>
//         </Box>
//     );
// }































// import * as React from 'react';
// import { Link, Outlet } from 'react-router-dom';
// import { styled, useTheme } from '@mui/material/styles';

// import Box from '@mui/material/Box';
// import MuiDrawer from '@mui/material/Drawer';
// import MuiAppBar from '@mui/material/AppBar';
// import Toolbar from '@mui/material/Toolbar';
// import List from '@mui/material/List';
// import Typography from '@mui/material/Typography';
// import CssBaseline from '@mui/material/CssBaseline';
// import Divider from '@mui/material/Divider';
// import IconButton from '@mui/material/IconButton';
// import ListItem from '@mui/material/ListItem';
// import ListItemButton from '@mui/material/ListItemButton';
// import ListItemIcon from '@mui/material/ListItemIcon';
// import ListItemText from '@mui/material/ListItemText';

// import MenuIcon from '@mui/icons-material/Menu';
// import ChevronLeftIcon from '@mui/icons-material/ChevronLeft';
// import ChevronRightIcon from '@mui/icons-material/ChevronRight';
// import PersonOutlinedIcon from '@mui/icons-material/PersonOutlined';
// import GroupOutlinedIcon from '@mui/icons-material/GroupOutlined';;

// import { DASHBOARD_ENDPOINT } from '../../config';


// // ==================================================
// // 1. CONSTANTS
// // ==================================================

// const DRAWER_WIDTH = 240;


// // ==================================================
// // 2. SHARED STYLES
// // ==================================================

// const listButtonIconStyles = {
//     width: 25,
//     height: 25,
//     color: 'var(--text-main)',
// };

// const listButtonTextStyles = {
//     fontSize: 'var(--fs-base)',
//     color: 'var(--text-main)',
// };

// const dashboardBrandStyles = {
//     fontSize: 'var(--fs-xl)',
//     color: 'var(--text-inverse)',
//     fontWeight: 'var(--fw-semibold)',
//     textDecoration: 'none',
//     transition: 'opacity 0.2s ease-in-out',

//     '&:hover': {
//         opacity: 0.8,
//     },
// };


// // ==================================================
// // 3. DRAWER WIDTH STYLES
// // ==================================================

// const openedMixin = (theme) => ({
//     width: DRAWER_WIDTH,

//     transition: theme.transitions.create('width', {
//         easing: theme.transitions.easing.sharp,
//         duration: theme.transitions.duration.enteringScreen,
//     }),

//     overflowX: 'hidden',
// });

// const closedMixin = (theme) => ({
//     width: `calc(${theme.spacing(7)} + 1px)`,

//     transition: theme.transitions.create('width', {
//         easing: theme.transitions.easing.sharp,
//         duration: theme.transitions.duration.leavingScreen,
//     }),

//     overflowX: 'hidden',

//     [theme.breakpoints.up('sm')]: {
//         width: `calc(${theme.spacing(8)} + 1px)`,
//     },
// });


// // ==================================================
// // 4. STYLED MUI COMPONENTS
// // ==================================================

// const DrawerHeader = styled('div')(({ theme }) => ({
//     display: 'flex',
//     alignItems: 'center',
//     padding: theme.spacing(0, 1),

//     // Match the height of the AppBar toolbar.
//     ...theme.mixins.toolbar,
// }));

// const AppBar = styled(MuiAppBar, {
//     shouldForwardProp: (prop) => prop !== 'open',
// })(({ theme }) => ({
//     zIndex: theme.zIndex.drawer + 1,

//     transition: theme.transitions.create(['width', 'margin'], {
//         easing: theme.transitions.easing.sharp,
//         duration: theme.transitions.duration.leavingScreen,
//     }),

//     variants: [
//         {
//             props: ({ open }) => open,

//             style: {
//                 marginLeft: DRAWER_WIDTH,
//                 width: `calc(100% - ${DRAWER_WIDTH}px)`,

//                 transition: theme.transitions.create(['width', 'margin'], {
//                     easing: theme.transitions.easing.sharp,
//                     duration: theme.transitions.duration.enteringScreen,
//                 }),
//             },
//         },
//     ],
// }));

// const Drawer = styled(MuiDrawer, {
//     shouldForwardProp: (prop) => prop !== 'open',
// })(({ theme }) => ({
//     width: DRAWER_WIDTH,
//     flexShrink: 0,
//     whiteSpace: 'nowrap',
//     boxSizing: 'border-box',

//     // Remove the vertical border between the drawer and content.
//     '& .MuiDrawer-paper': {
//         borderRight: 0,
//     },

//     variants: [
//         {
//             props: ({ open }) => open,

//             style: {
//                 ...openedMixin(theme),

//                 '& .MuiDrawer-paper': {
//                     ...openedMixin(theme),
//                 },
//             },
//         },
//         {
//             props: ({ open }) => !open,

//             style: {
//                 ...closedMixin(theme),

//                 '& .MuiDrawer-paper': {
//                     ...closedMixin(theme),
//                 },
//             },
//         },
//     ],
// }));


// // ==================================================
// // 5. NAVIGATION CONFIGURATION
// // ==================================================

// const drawerNavigationData = [
//     {
//         id: 1,
//         name: 'Accounts',
//         link: `${DASHBOARD_ENDPOINT}/accounts`,
//         icon: GroupOutlinedIcon,
//     },
// ];


// // ==================================================
// // 6. REUSABLE COMPONENTS
// // ==================================================

// const DashboardBrand = ({ sx = {} }) => (
//     <Typography
//         component={Link}
//         to={DASHBOARD_ENDPOINT}
//         sx={[dashboardBrandStyles, sx]}
//     >
//         Dashboard
//     </Typography>
// );

// const DrawerToggleButton = ({ open, onOpen }) => (
//     <IconButton
//         aria-label="open drawer"
//         edge="start"
//         onClick={onOpen}
//         sx={{
//             marginRight: 4,
//             display: open ? 'none' : 'inline-flex',
//             color: 'var(--text-inverse)',

//             '&:hover': {
//                 backgroundColor: 'var(--bg-hover-mui-30)',
//             },
//         }}
//     >
//         <img src="/logoWhite.png" alt="logo" width="25" height="25" />
//         <MenuIcon sx={{...listButtonIconStyles, color: 'var(--text-inverse)' }} />
//     </IconButton>
// );

// const DrawerCloseButton = ({ open, onClose }) => {
//     const theme = useTheme();

//     return (
//         <IconButton
//             aria-label="close drawer"
//             onClick={onClose}
//             sx={{
//                 color: 'var(--text-inverse)',
//                 display: open ? 'inline-flex' : 'none',

//                 '&:hover': {
//                     backgroundColor: 'var(--bg-hover-mui-30)',
//                 },
//             }}
//         >
//             {theme.direction === 'rtl' ? (
//                 <ChevronRightIcon sx={{...listButtonIconStyles, color: 'var(--text-inverse)' }} />
//             ) : (
//                 <ChevronLeftIcon sx={{...listButtonIconStyles, color: 'var(--text-inverse)' }} />
//             )}
//         </IconButton>
//     );
// };

// const DashboardNavigationItem = ({ item, open }) => {
//     const Icon = item.icon;

//     return (
//         <ListItem disablePadding sx={{ display: 'block' }}>
//             <ListItemButton
//                 component={Link}
//                 to={item.link}
//                 sx={{
//                     minHeight: 48,
//                     px: 2.5,
//                     justifyContent: open ? 'initial' : 'center',
//                 }}
//             >
//                 <ListItemIcon
//                     sx={{
//                         minWidth: 0,
//                         justifyContent: 'center',
//                         mr: open ? 3 : 'auto',
//                     }}
//                 >
//                     {Icon && <Icon sx={listButtonIconStyles} />}
//                 </ListItemIcon>

//                 <ListItemText
//                     primary={item.name}
//                     slotProps={{
//                         primary: {
//                             sx: listButtonTextStyles,
//                         },
//                     }}
//                     sx={{
//                         opacity: open ? 1 : 0,
//                     }}
//                 />
//             </ListItemButton>
//         </ListItem>
//     );
// };

// const DashboardNavigation = ({ open }) => (
//     <List sx={{padding: 0}}>
//         {drawerNavigationData.map((item) => (
//             <DashboardNavigationItem
//                 key={item.id}
//                 item={item}
//                 open={open}
//             />
//         ))}
//     </List>
// );

// const DashboardAppBar = ({ open, onOpen }) => (
//     <AppBar
//         position="fixed"
//         open={open}
//         sx={{
//             backgroundColor: 'var(--bg-inverse)',
//             boxShadow: 'none',
//         }}
//     >
//         <Toolbar
//             sx={{
//                 display: 'flex',
//                 justifyContent: 'space-between',
//             }}
//         >
//             <Box
//                 sx={{
//                     display: 'flex',
//                     alignItems: 'center',
//                 }}
//             >
//                 <DrawerToggleButton
//                     open={open}
//                     onOpen={onOpen}
//                 />

//                 <DashboardBrand
//                     sx={{
//                         display: open ? 'none' : 'block',
//                     }}
//                 />
//             </Box>
//         </Toolbar>
//     </AppBar>
// );

// const DashboardDrawer = ({ open, onClose }) => (
//     <Drawer variant="permanent" open={open}>
//         <DrawerHeader
//             sx={{
//                 justifyContent: 'space-between',
//                 backgroundColor: 'var(--bg-inverse)',
//             }}
//         >
//             <DashboardBrand
//                 sx={{
//                     display: open ? 'block' : 'none',
//                     paddingLeft: 1.5,
//                 }}
//             />

//             <DrawerCloseButton
//                 open={open}
//                 onClose={onClose}
//             />
//         </DrawerHeader>

//         <Divider />

//         <DashboardNavigation open={open} />
//     </Drawer>
// );

// const DashboardContent = () => (
//     <Box
//         component="main"
//         sx={{
//             flexGrow: 1,
//             p: 3,
//         }}
//     >
//         <DrawerHeader />
//         <Outlet />
//         <footer>footer</footer>
//     </Box>
// );


// // ==================================================
// // 7. MAIN DASHBOARD LAYOUT
// // ==================================================

// export default function Dashboard() {
//     const [open, setOpen] = React.useState(true);

//     const handleDrawerOpen = () => {
//         setOpen(true);
//     };

//     const handleDrawerClose = () => {
//         setOpen(false);
//     };

//     return (
//         <Box sx={{ display: 'flex' }}>
//             <CssBaseline />

//             <DashboardAppBar
//                 open={open}
//                 onOpen={handleDrawerOpen}
//             />

//             <DashboardDrawer
//                 open={open}
//                 onClose={handleDrawerClose}
//             />

//             <DashboardContent />
//         </Box>
//     );
// }






















import { useState } from "react";
import { Outlet, Link as RouterLink } from "react-router-dom";

import Link from "@mui/material/Link";
import IconButton from '@mui/material/IconButton';
import List from "@mui/material/List";
import ListItem from "@mui/material/ListItem";
import ListItemButton from "@mui/material/ListItemButton";
import ListItemIcon from "@mui/material/ListItemIcon";

import ListItemText from "@mui/material/ListItemText";

import Divider from '@mui/material/Divider';

// lucide icons
import { UsersRound, PanelLeftOpen, PanelRightOpen, Tags, PackageCheck } from "lucide-react";

// constant styles
import { iconsStyles } from "./dashboardStyle";

import { DASHBOARD_ENDPOINT } from '../../config'
import styles from "./dashboard.module.css"

export default function Dashboard() {
    const [open, setOpen] = useState(true);

    const navigationData = [
        {
            id: 1,
            name: 'Accounts',
            link: `${DASHBOARD_ENDPOINT}/accounts`,
            icon: UsersRound,
        },
        {
            id: 2,
            name: 'Orders',
            link: `${DASHBOARD_ENDPOINT}/orders`,
            icon: PackageCheck,
        },
        {
            id: 3,
            name: 'Products',
            link: `${DASHBOARD_ENDPOINT}/products`,
            icon: Tags,
        },
    ];

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
                                "&:hover": { backgroundColor: "transparent" },
                            }}
                            className={`${styles.menuButton}`}
                            onClick={() => setOpen(!open)}
                        >
                            <PanelLeftOpen size={iconsStyles.size} color={iconsStyles.color_inverse} />
                            <img src="/logoWhite.png" alt="logo" width="25px" />
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
                            Dashboard
                        </Link>
                    </div>
                    <div className={styles.headerRight}></div>
                </nav>
            </header>
            <aside className={`${styles.drawer} ${styles.transition} ${open ? styles.drawerOpen : ""}`}>
                <div className={`layout-wrapper ${styles.drawerHeader}`}>
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
                        onClick={() => setOpen(!open)}
                    >
                        <PanelRightOpen size={iconsStyles.size} color={iconsStyles.color_inverse} />
                    </IconButton>
                </div>
                <Divider />
                <List sx={{ width: "100%", padding: 0 }}>
                    {navigationData.map((item) => (
                        <ListItem key={item.id} disablePadding sx={{ display: 'block' }}>
                            <ListItemButton
                                component={RouterLink}
                                to={item.link}
                                sx={[
                                    {
                                        minHeight: 48,
                                        px: 3.5,
                                    },
                                    open
                                        ? {
                                            justifyContent: 'initial',
                                        }
                                        : {
                                            justifyContent: 'center',
                                        },
                                ]}
                            >
                                <ListItemIcon
                                    sx={[
                                        {
                                            minWidth: 0,
                                            justifyContent: 'center',
                                        },
                                        open
                                            ? {
                                                mr: 3,
                                            }
                                            : {
                                                mr: 'auto',
                                            },
                                    ]}
                                >
                                    {item.icon && <item.icon size={iconsStyles.size} color={iconsStyles.color_main} />}
                                </ListItemIcon>
                                <ListItemText
                                    primary={item.name}
                                    sx={{
                                        opacity: open ? 1 : 0,
                                        "& .MuiListItemText-primary": {
                                            fontSize: "var(--fs-sm)",
                                            fontWeight: "var(--fw-regular)",
                                            color: "var(--text-main)",
                                        },
                                    }}
                                />
                            </ListItemButton>
                        </ListItem>
                    ))}
                </List>
            </aside>
            <main className={styles.main}>
                <Outlet />
                <footer className={styles.footer}>Footer</footer>
            </main>
        </div>
    )
}