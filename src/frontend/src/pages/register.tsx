import { useEffect, useState } from "react";
import AuthService from "../services/auth-service";
import InputField from "../components/input-field";
import Box from '@mui/material/Box';
import InputPassword from "../components/input-password";
import Text from "../components/text";
import Divider from '@mui/material/Divider';
import Link from '@mui/material/Link';
import Button from '@mui/material/Button';
import {WebsiteLogo} from "../components/website-logo";
import Alert from '@mui/material/Alert';
import { ThemeProvider } from "@emotion/react";
import { MyTheme } from "../theme-mui";
import { useNavigate } from "react-router-dom";


export function RegisterPage() {
  const [login, setLogin] = useState<string>("");
  const [password, setPassword] = useState<string>("");
  const [email, setEmail] = useState<string>("");
  const [phone, setPhone] = useState<string>("");
  const [lastname, setLastname] = useState<string>("");
  const [firstname, setFirstname] = useState<string>("");
  const [errorMsg, setErrorMsg] = useState<string>("");
  const navigate = useNavigate();

  const auth = async () => {
    if (login && password && email && phone && lastname && firstname) {
      const response = await AuthService.register({
        login, password, email, phone, lastname, firstname
      });

      if (response) {
        setErrorMsg(response);
      } else {
        navigate("/");
      }
    } else {
      setErrorMsg("Ошибка: Не все поля заполнены");
    }
  }; //  border border-red-700

  useEffect(() => {
    if (AuthService.isAuth()) {
      navigate("/");
    }
  });

  return (
    <div className="flex justify-center items-center h-screen bg-my-primary-color">
      <Box
        className="flex flex-col gap-3 text-wrap bg-my-third-color rounded-md p-6 max-w-md"
        component="form"
      >
        <WebsiteLogo size={"high"} />

        <Text
          size="large"
          className="flex justify-center mt-7 mb-1 text-my-secondary-color text-my-large-size"
        >
          Зарегистрироваться
        </Text>

        <div className="grid grid-cols-2 gap-4">
          <InputField isRequired={true} label="Логин" value={login} setValue={(value: string) => {
            setLogin(value);
          }}/>
          <InputField isRequired={true} label="Пароль" value={password} setValue={(value: string) => {
            setPassword(value);
          }}/>
          <InputField isRequired={true} label="Почта" value={email} setValue={(value: string) => {
            setEmail(value);
          }}/>
          <InputField isRequired={true} label="Телефон" value={phone} setValue={(value: string) => {
            setPhone(value);
          }}/>
          <InputField isRequired={true} label="Фамилия" value={lastname} setValue={(value: string) => {
            setLastname(value);
          }}/>
          <InputField isRequired={true} label="Имя" value={firstname} setValue={(value: string) => {
            setFirstname(value);
          }}/>
        </div>

        {errorMsg &&
          <Alert
            sx={{fontWeight: 1000}}
            severity="error"
          >
            {errorMsg}
          </Alert>
        }
        
        <ThemeProvider theme={MyTheme}>
          <Button
            sx={{
              marginTop: 5,
              fontSize: "var(--my-medium-size)"
            }}
            color="secondary"
            size="small"
            variant="outlined"
            onClick={ auth }
          >
            Готово
          </Button>
        </ThemeProvider>

        <Divider sx={{ borderBottomWidth: 3 }} variant="middle" />
        
        <ThemeProvider theme={MyTheme}>
          <Link
            className="flex justify-center"
            color="secondary"
            sx={{fontSize: "var(--my-little-size)"}}
            href="/login"
            underline="hover"
          >
            Залогиниться
          </Link>
        </ThemeProvider>
      </Box>
    </div>
  )
}
