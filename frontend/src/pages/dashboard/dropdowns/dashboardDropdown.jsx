
import { useState, useRef, useEffect } from 'react';
import { Link as RouterLink } from 'react-router-dom';

import ListItemButton from '@mui/material/ListItemButton';
import MenuItem from '@mui/material/MenuItem';

import HoverMenu from 'material-ui-popup-state/HoverMenu';
import {
    usePopupState,
    bindHover,
    bindMenu,
} from 'material-ui-popup-state/hooks';

import styles from './dashboardDropdown.module.css';
import { iconsStyles, hoverStyles, menuBtnFont } from '../dashboardStyle';


const buttonStyles = {
    btn: {
        justifyContent: 'flex-start',
        width: '100%',
        minHeight: 48,
        px: 3.5,
    },
    itemBtn: {
        justifyContent: 'flex-start',
        width: '100%',
        pl: 3.2,
    },
    hover: {
        '&:hover': {
            backgroundColor: hoverStyles.mui_main,
        },
        '& .MuiTouchRipple-root': {
            color: hoverStyles.mui_ripple
        },
    },
    menuBtnFont: {
        ...menuBtnFont.alignMent,
        fontSize: menuBtnFont.size,
        fontWeight: menuBtnFont.weight,
        color: menuBtnFont.color_main,
        textTransform: menuBtnFont.textTransform,
        transition: 'opacity 0.2s ease',
    }
};

// Child item
function DashboardDropdownChild({
    item,
    collapsed = false,
    setOpen,
    updateState = false,
    closePopup
}) {
    const Icon = item.icon;

    const handleClick = () => {
        closePopup?.();

        if (updateState) {
            setOpen(false);
        }
    }

    const content = (
        <>
            {Icon && (
                <Icon
                    className={
                        collapsed
                            ? styles.popupIcon
                            : styles.childIcon
                    }
                    size={iconsStyles.size}
                    color={iconsStyles.color_main}
                />

            )}

            {item.name && (
                <span style={buttonStyles.menuBtnFont}>
                    {item.name}
                </span>
            )}
        </>
    );

    if (collapsed) {
        return (
            <MenuItem
                sx={buttonStyles.hover}
                component={item.link ? RouterLink : 'li'}
                {...(item.link ? { to: item.link } : {})}
                onClick={handleClick}
            >
                {content}
            </MenuItem>
        );
    }

    return (
        <ListItemButton
            sx={{...buttonStyles.itemBtn, ...buttonStyles.hover}}
            className={styles.menuItem}
            component={item.link ? RouterLink : 'div'}
            {...(item.link ? { to: item.link } : {})}
            onClick={handleClick}
        >
            {content}
        </ListItemButton>
    );
}


// Parent item
function DashboardDropdownNode({
    item,
    open,
    treeMenuOpen,
    setTreeMenuOpen,
    updateState,
    setOpen,
}) {
    const popupState = usePopupState({
        variant: 'popover',
        popupId: `hover-menu-${item.id}`,
    });

    const Icon = item.icon;
    const hasChildren = Boolean(item.child?.length);
    const isTreeOpen = treeMenuOpen === item.id;

    useEffect(() => {
        if (open || !hasChildren) {
            popupState.close();
        }
    }, [open, hasChildren]);

    function handleClick() {
        if (updateState && !hasChildren) {
            setOpen(false);
        }

        if (!open || !hasChildren) return;

        setTreeMenuOpen((current) =>
            current === item.id ? null : item.id
        );
    }

    return (
        <div className={styles.parent}>
            {/* One parent button for both sidebar states */}
            <ListItemButton
                sx={{...buttonStyles.btn, ...buttonStyles.hover}}
                className={styles.btn}
                component={item.link ? RouterLink : 'div'}
                {...(item.link ? { to: item.link } : {})}
                {...(
                    !open && hasChildren
                        ? bindHover(popupState)
                        : {}
                )}
                onClick={handleClick}
                aria-expanded={
                    hasChildren && open
                        ? isTreeOpen
                        : undefined
                }
            >
                {Icon && (
                    <Icon
                        className={styles.parentIcon}
                        size={iconsStyles.size}
                        color={iconsStyles.color_main}
                    />
                )}

                {item.name && (
                    <span
                        style={{
                            ...buttonStyles.menuBtnFont,
                            opacity: open ? 1 : 0,
                            pointerEvents: open ? 'auto' : 'none',
                        }}
                    >
                        {item.name}
                    </span>
                )}
            </ListItemButton>

            {/* Expanded sidebar: inline tree */}
            {open && hasChildren && (
                <div
                    className={[
                        styles.menu,
                        isTreeOpen ? styles.menuOpen : '',
                    ].join(' ')}
                >
                    {item.child.map((child) => (
                        <DashboardDropdownChild
                            key={child.id}
                            item={child}
                            setOpen={setOpen}
                            updateState={updateState}
                        />
                    ))}
                </div>
            )}

            {/* Collapsed sidebar: hover popup */}
            {!open && hasChildren && (
                <HoverMenu
                    {...bindMenu(popupState)}
                    anchorOrigin={{
                        vertical: 'bottom',
                        horizontal: 'right',
                    }}
                    transformOrigin={{
                        vertical: 'top',
                        horizontal: 'left',
                    }}
                    slotProps={{
                        paper: {
                            sx: {
                                borderRadius: '12px',
                                mt: '-37px',
                                backgroundColor: "var(--bg-main)",
                                boxShadow: "var(--shadow-mui)"
                            },
                        },
                    }}
                >
                    {item.child.map((child) => (
                        <DashboardDropdownChild
                            key={child.id}
                            item={child}
                            collapsed
                            closePopup={popupState.close}
                        />
                    ))}
                </HoverMenu>
            )}
        </div>
    );
}


// Main component
function DashboardDropdown({ data, open, setOpen, updateState, ...props }) {
    const [treeMenuOpen, setTreeMenuOpen] = useState(null);
    const treeRef = useRef(null);

    useEffect(() => {
        function handleClickOutside(event) {
            if (
                treeRef.current &&
                !treeRef.current.contains(event.target)
            ) {
                setTreeMenuOpen(null);
            }
        }

        document.addEventListener(
            'mousedown',
            handleClickOutside
        );

        return () => {
            document.removeEventListener(
                'mousedown',
                handleClickOutside
            );
        };
    }, []);

    // Close inline trees when the sidebar collapses
    useEffect(() => {
        if (!open) {
            setTreeMenuOpen(null);
        }
    }, [open]);

    return (
        <div
            className={styles.container}
            ref={treeRef}
            {...props}
        >
            {data.map((item) => (
                <DashboardDropdownNode
                    key={item.id}
                    item={item}
                    open={open}
                    treeMenuOpen={treeMenuOpen}
                    setTreeMenuOpen={setTreeMenuOpen}
                    updateState={updateState}
                    setOpen={setOpen}
                />
            ))}
        </div>
    );
}

export default DashboardDropdown;
