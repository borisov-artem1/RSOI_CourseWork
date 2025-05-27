import { createTheme } from "@mui/material/styles";

export const MyTheme = createTheme({
  cssVariables: true,
  palette: {
    primary: {
      main: "#2f855a", /* tailwind: indigo-500 */
    },
    secondary: {
      main: "#a0aec0", /* tailwind: slate-500 */
    },
  },
});
