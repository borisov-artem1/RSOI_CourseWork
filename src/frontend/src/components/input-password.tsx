import React from 'react'
import IconButton from '@mui/material/IconButton';
import FilledInput from '@mui/material/FilledInput';
import InputLabel from '@mui/material/InputLabel';
import InputAdornment from '@mui/material/InputAdornment';
import FormControl from '@mui/material/FormControl';
import Visibility from '@mui/icons-material/Visibility';
import VisibilityOff from '@mui/icons-material/VisibilityOff';
import { ThemeProvider } from '@mui/material';
import { MyTheme } from '../theme-mui';

interface InputPasswordProps {
  value: string;
  setValue: (value: string) => void;
}

export default function InputPassword(props: InputPasswordProps) {
  const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    props.setValue(event.target.value);
  }

  const [showPassword, setShowPassword] = React.useState(false);

  const handleClickShowPassword = () => setShowPassword((show) => !show);

  const handleMouseDownPassword = (event: React.MouseEvent<HTMLButtonElement>) => {
    event.preventDefault();
  };

  const handleMouseUpPassword = (event: React.MouseEvent<HTMLButtonElement>) => {
    event.preventDefault();
  };

  return (
    <ThemeProvider theme={MyTheme}>
      <FormControl variant="filled">
        <InputLabel htmlFor="filled-adornment-password">Пароль</InputLabel>
        <FilledInput
          id="filled-adornment-password"
          color="primary"
          type={showPassword ? 'text' : 'password'}
          value={props.value}
          onChange={handleChange}
          endAdornment={
            <InputAdornment position="end">
              <IconButton
                aria-label="toggle password visibility"
                onClick={handleClickShowPassword}
                onMouseDown={handleMouseDownPassword}
                onMouseUp={handleMouseUpPassword}
                edge="end"
              >
                {showPassword ? <VisibilityOff /> : <Visibility />}
              </IconButton>
            </InputAdornment>
          }
        />
      </FormControl>
    </ThemeProvider>
  )
}
