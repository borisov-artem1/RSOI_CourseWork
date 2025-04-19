import React from 'react';
import TextField from '@mui/material/TextField';
import { ThemeProvider } from "@mui/material/styles";
import {MyTheme} from "../theme-mui";

interface InputFieldProps {
  label: string;
  value: string;
  isRequired?: boolean;
  setValue: (value: string) => void;
  className?: string;
}

export default function InputField({
  label,
  value, 
  setValue,
  className,
  isRequired = false,
}: InputFieldProps) {
  const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setValue(event.target.value);
  }

  return (
    <ThemeProvider theme={MyTheme}>
      <TextField
        required={isRequired}
        id="filled-required"
        label={label}
        variant="filled"
        value={value}
        className={className}
        onChange={handleChange}
      />
    </ThemeProvider>
  )
}
