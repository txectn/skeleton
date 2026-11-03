// // components/UploadImage.jsx
// import { useEffect, useRef, useState } from "react";

// import Box from "@mui/material/Box";
// import Typography from "@mui/material/Typography";

// import { CloudUpload } from "lucide-react";

// export default function UploadImage({
//     setData,
//     width = "100%",
//     height = "200px",
//     bgColor = "transparent",
//     border = "1px dashed",
//     borderColor = {
//         init: "var(--border-color)",
//         hover: "var(--brand-primary)"
//     },
//     focusBorder="2px solid",
//     borderRadius="2px",
//     fontSize="var(--fs-sm)",
//     fontWeight="var(--fw-medium)",
//     color="var(--text-muted-100)",
//     iconSize="40px",
//     style = {},
//     typography1Style = {display: "none"},
//     typography2Style = {},
//     showPreview = true,
// }) {
//     const inputRef = useRef(null);
//     const [file, setFile] = useState(null);
//     const [isDragging, setIsDragging] = useState(false);
//     const [preview, setPreview] = useState("");

//     useEffect(() => {
//         if (!file) {
//             setPreview("");
//             return;
//         }

//         const objectUrl = URL.createObjectURL(file);
//         setPreview(objectUrl);

//         return () => URL.revokeObjectURL(objectUrl);
//     }, [file]);

//     const selectImage = (selectedFile) => {
//         if (!selectedFile || !selectedFile.type.startsWith("image/")) {
//             return;
//         }

//         setFile(selectedFile);
//         setData?.(selectedFile);
//     };

//     const handleInputChange = (event) => {
//         selectImage(event.target.files?.[0]);

//         // Allow selecting the same image again.
//         event.target.value = "";
//     };

//     const handleDrop = (event) => {
//         event.preventDefault();
//         setIsDragging(false);

//         const droppedFile = event.dataTransfer.files?.[0];
//         selectImage(droppedFile);
//     };

//     const handleKeyDown = (event) => {
//         if (event.key === "Enter" || event.key === " ") {
//             event.preventDefault();
//             inputRef.current?.click();
//         }
//     };

//     return (
//         <Box
//             role="button"
//             tabIndex={0}
//             aria-label="Upload an image"
//             onClick={() => inputRef.current?.click()}
//             onKeyDown={handleKeyDown}
//             onDragOver={(event) => {
//                 event.preventDefault();
//                 setIsDragging(true);
//             }}
//             onDragLeave={(event) => {
//                 if (!event.currentTarget.contains(event.relatedTarget)) {
//                     setIsDragging(false);
//                 }
//             }}
//             onDrop={handleDrop}
//             sx={{
//                 width,
//                 height,
//                 boxSizing: "border-box",
//                 position: "relative",
//                 overflow: "hidden",

//                 display: "flex",
//                 flexDirection: "column",
//                 alignItems: "center",
//                 justifyContent: "center",
//                 gap: 1,

//                 border: border,
//                 borderColor: isDragging
//                     ? borderColor.hover
//                     : borderColor.init,
//                 borderRadius: borderRadius,
//                 backgroundColor: bgColor,
//                 cursor: "pointer",
//                 transition: "border-color 0.2s, background-color 0.2s",

//                 ...(isDragging && {
//                     backgroundColor: "var(--bg-surface)",
//                 }),

//                 "&:hover": {
//                     borderColor: borderColor.hover,
//                 },

//                 "&:focus-visible": {
//                     outline: focusBorder,
//                     outlineColor: borderColor.hover,
//                     outlineOffset: 2,
//                 },
//                 ...style,
//             }}
//         >
//             <input
//                 ref={inputRef}
//                 type="file"
//                 accept="image/*"
//                 hidden
//                 onChange={handleInputChange}
//             />

//             {showPreview && preview ? (
//                 <Box
//                     component="img"
//                     src={preview}
//                     alt="Selected image preview"
//                     sx={{
//                         width: "100%",
//                         height: "100%",
//                         objectFit: "contain",
//                         p: 1,
//                         boxSizing: "border-box",
//                     }}
//                 />
//             ) : (
//                 <>
//                     <CloudUpload size={iconSize} color={color} />

//                     <Typography
//                         variant="body2"
//                         textAlign="center"
//                         sx={{
//                             ...typography1Style, 
//                             color: color,
//                             fontSize: fontSize,
//                             fontWeight: fontWeight,
//                         }}
//                     >
//                         Drag and drop an image here <br /> or click to browse
//                     </Typography>

//                     <Typography
//                         variant="caption"
//                         color="text.secondary"
//                         textAlign="center"
//                         sx={{
//                             ...typography2Style,
//                             color: color,
//                             fontSize: fontSize,
//                             fontWeight: fontWeight
//                         }}
//                     >
//                         Upload an image
//                     </Typography>
//                 </>
//             )}
//         </Box>
//     );
// }







import { useEffect, useRef, useState } from "react";

import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";

import { CloudUpload } from "lucide-react";

export default function UploadImage({
    setData,
    type = "number",
    width = "100%",
    height = "200px",
    bgColor = "transparent",
    border = "1px dashed",
    borderColor = {
        init: "var(--border-color)",
        hover: "var(--brand-primary)",
    },
    focusBorder = "2px solid",
    borderRadius = "2px",
    fontSize = "var(--fs-sm)",
    fontWeight = "var(--fw-medium)",
    color = "var(--text-muted-100)",
    iconSize = "40px",
    style = {},
    typography1Style = { display: "none" },
    typography2Style = {},
    showPreview = true,
}) {
    const inputRef = useRef(null);
    const [file, setFile] = useState(null);
    const [isDragging, setIsDragging] = useState(false);
    const [preview, setPreview] = useState("");

    useEffect(() => {
        if (!file) {
            setPreview("");
            return;
        }

        const objectUrl = URL.createObjectURL(file);
        setPreview(objectUrl);

        return () => URL.revokeObjectURL(objectUrl);
    }, [file]);

    const selectImage = (selectedFile) => {
        if (
            !selectedFile ||
            !selectedFile.type.startsWith("image/")
        ) {
            return;
        }

        setFile(selectedFile);

        if (type === "array") {
            setData?.((prev) => [
                ...(Array.isArray(prev) ? prev : []),
                selectedFile,
            ]);
        } else if (type === "object") {
            setData?.({
                image: selectedFile,
            });
        } else if (type === "number") {
            setData?.(selectedFile);
        }
    };

    const handleInputChange = (event) => {
        selectImage(event.target.files?.[0]);
        event.target.value = "";
    };

    const handleDrop = (event) => {
        event.preventDefault();
        setIsDragging(false);

        const droppedFile = event.dataTransfer.files?.[0];
        selectImage(droppedFile);
    };

    const handleKeyDown = (event) => {
        if (event.key === "Enter" || event.key === " ") {
            event.preventDefault();
            inputRef.current?.click();
        }
    };

    return (
        <Box
            role="button"
            tabIndex={0}
            aria-label="Upload an image"
            onClick={() => inputRef.current?.click()}
            onKeyDown={handleKeyDown}
            onDragOver={(event) => {
                event.preventDefault();
                setIsDragging(true);
            }}
            onDragLeave={(event) => {
                if (
                    !event.currentTarget.contains(
                        event.relatedTarget
                    )
                ) {
                    setIsDragging(false);
                }
            }}
            onDrop={handleDrop}
            sx={{
                width,
                height,
                boxSizing: "border-box",
                position: "relative",
                overflow: "hidden",
                display: "flex",
                flexDirection: "column",
                alignItems: "center",
                justifyContent: "center",
                gap: 1,
                border,
                borderColor: isDragging
                    ? borderColor.hover
                    : borderColor.init,
                borderRadius,
                backgroundColor: bgColor,
                cursor: "pointer",
                transition:
                    "border-color 0.2s, background-color 0.2s",

                ...(isDragging && {
                    backgroundColor: "var(--bg-surface)",
                }),

                "&:hover": {
                    borderColor: borderColor.hover,
                },

                "&:focus-visible": {
                    outline: focusBorder,
                    outlineColor: borderColor.hover,
                    outlineOffset: 2,
                },

                ...style,
            }}
        >
            <input
                ref={inputRef}
                type="file"
                accept="image/*"
                hidden
                onChange={handleInputChange}
            />

            {showPreview && preview ? (
                <Box
                    component="img"
                    src={preview}
                    alt="Selected image preview"
                    sx={{
                        width: "100%",
                        height: "100%",
                        objectFit: "contain",
                        p: 1,
                        boxSizing: "border-box",
                    }}
                />
            ) : (
                <>
                    <CloudUpload
                        size={iconSize}
                        color={color}
                    />

                    <Typography
                        variant="body2"
                        textAlign="center"
                        sx={{
                            ...typography1Style,
                            color,
                            fontSize,
                            fontWeight,
                        }}
                    >
                        Drag and drop an image here
                        <br />
                        or click to browse
                    </Typography>

                    <Typography
                        variant="caption"
                        textAlign="center"
                        sx={{
                            ...typography2Style,
                            color,
                            fontSize,
                            fontWeight,
                        }}
                    >
                        Upload an image
                    </Typography>
                </>
            )}
        </Box>
    );
}
