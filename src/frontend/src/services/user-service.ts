import { AxiosResponse } from "axios";
import { UserInterface } from "../model/interface/user.interface";
import {$apiUser} from "../http";

export default class UserService {
  static async fetchUsers(): Promise<AxiosResponse<UserInterface[]>> {
    return $apiUser.get<UserInterface[]>('/user/');
  }

  static async getMe(): Promise<UserInterface | undefined> {
    try {
      const response = await $apiUser.get<UserInterface>('/user/me/');
      const user = response.data;

      return user;
    } catch (e) {
      console.log(e);
    }
  }
}
