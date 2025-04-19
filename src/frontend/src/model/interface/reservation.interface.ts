import { BookInterface } from "../interface/book.interface";
import { LibraryInterface } from "../interface/library.interface";

export type ReservationStatusType = "RENTED" | "RETURNED" | "EXPIRED" | "";


export interface ReservationInterface {
  reservationUid: string;
  username: string;
  status: ReservationStatusType;
  startDate: string;
  tillDate: string;
  library: LibraryInterface;
  book: BookInterface;
}

export interface ReservationResponseInterface {
  items: ReservationInterface[];
  page: number;
  pageSize: number;
  totalElements: number;
}

export interface ReservationFilter {
  status?: ReservationStatusType;
  page?: number;
  size?: number;
}
