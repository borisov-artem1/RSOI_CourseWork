import { createTheme } from "@mui/material/styles";

export const MyTheme = createTheme({
  cssVariables: true,
  palette: {
    primary: {
      main: "#6366f1", /* tailwind: indigo-500 */
    },
    secondary: {
      main: "#64748b", /* tailwind: slate-500 */
    },
  },
});
