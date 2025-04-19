import { AxiosResponse, isAxiosError } from "axios";
import {$apiAuth} from "../http";
import { AuthResponse } from "../model/response/auth.response";
import UserService from "./user-service";

interface CreateUserDto {
  login: string;
  password: string;
  email: string;
  phone: string;
  lastname: string;
  firstname: string;
  role?: "USER" | "MODERATOR" | "ADMIN";
}

export default class AuthService {
  static async login(login: string, password: string): Promise<string | null>  {
    const response = await $apiAuth.post<AuthResponse>(
      "user/login/",
      {login, password},
    ).catch((error) => {
      var errorMessage: string;
      if (isAxiosError(error)) {
        if (error.response) {
          errorMessage = `${error.response.data.message}`;
          if (error.response.status === 400) {
            errorMessage += (`: ${error.response.data.errors[0].loc} - `
              +`${error.response.data.errors[0].msg}`);
          }
        } else {
          errorMessage = `${error}`;
        }
        console.log(error);
      } else {
        errorMessage = `NOT AXIOS: ${error}`;
        console.log(`NOT AXIOS: ${error}`);
      }

      return errorMessage;
    });

    if (typeof response === "string") {
      return response;
    } else {
      localStorage.setItem(`accessToken`, response.data.access_token as string);
      localStorage.setItem(`refreshToken`, response.data.refresh_token as string);

      const user = await UserService.getMe();

      if (!user) {
        AuthService.logout();
        return "Ошибка: Не удалось получить данные пользователя";
      }

      localStorage.setItem(`userUuid`, user?.uuid as string);
      localStorage.setItem(`userLogin`, user?.login as string);
      localStorage.setItem(`userRole`, user?.role as string);

      return null;
    }
  }

  static async register({...registerDto}: CreateUserDto): Promise<string | null>  { 
    const response = await $apiAuth.post<AuthResponse>(
      "user/register/",
      {...registerDto, role: "USER"},
    ).catch((error) => {
      var errorMessage: string;
      if (isAxiosError(error)) {
        if (error.response) {
          errorMessage = `${error.response.data.message}`;
          if (error.response.status === 400) {
            errorMessage += (`: ${error.response.data.errors[0].loc} - `
              +`${error.response.data.errors[0].msg}`);
          }
        } else {
          errorMessage = `${error}`;
        }
        console.log(error);
      } else {
        errorMessage = `NOT AXIOS: ${error}`;
        console.log(`NOT AXIOS: ${error}`);
      }

      return errorMessage;
    });

    if (typeof response === "string") {
      return response;
    } else {
      localStorage.setItem(`accessToken`, response.data.access_token as string);
      localStorage.setItem(`refreshToken`, response.data.refresh_token as string);
      return null;
    }
  }

  static logout(): undefined {
    localStorage.clear();
    return;
  }

  static isAuth(): boolean {
    return !!localStorage.getItem(`accessToken`);
  }

  static isAdmin(): boolean {
    return AuthService.isAuth() && localStorage.getItem(`userRole`) === "ADMIN";
  }
}
