import { createTheme } from "@mui/material/styles";

export const MyTheme = createTheme({
  cssVariables: true,
  palette: {
    primary: {
      main: "#dd6b20", /* tailwind: indigo-500 */
    },
    secondary: {
      main: "#2d3748", /* tailwind: slate-500 */
    },
  },
});
