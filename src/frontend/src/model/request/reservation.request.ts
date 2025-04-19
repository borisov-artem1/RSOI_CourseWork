import {Dayjs} from "dayjs"
import { BookConditionType } from "../interface/book.interface";

export interface TakeBookRequest {
  libraryUuid: string;
  booUuid: string;
  tillDate: Dayjs;
}

export interface ReturnBook {
  reservationUuid: string;
  condition: BookConditionType;
  date: Dayjs;
}
