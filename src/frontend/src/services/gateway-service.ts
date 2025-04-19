import { isAxiosError } from "axios";
import {$apiGateway} from "../http";
import { BookFilter, BookResponseInterface } from "../model/interface/book.interface";
import { LibraryResponseInterface, LibraryFilter } from "../model/interface/library.interface";
import { ReturnBook, TakeBookRequest } from "../model/request/reservation.request";
import { TakeBookResponse } from "../model/response/reservation.response";
import { RatingInterface } from "../model/interface/rating.interface";
import { ReservationFilter, ReservationResponseInterface } from "../model/interface/reservation.interface";

export default class GatewayService {
  static async getLibraries(filters?: LibraryFilter): Promise<LibraryResponseInterface | undefined> {
    try {
      const response = await $apiGateway.get<LibraryResponseInterface>('/libraries/', {
        params: {
          city: filters?.city,
          page: filters?.page,
          size: filters?.size,
        }
      });
      const libraries = response.data;
      return libraries;
    } catch (e) {
      console.log(e);
    }
  }

  static async getBooksByLibraryUuid(libraryUuid: string, filters?: BookFilter): Promise<BookResponseInterface | undefined> {
    try {
      const response = await $apiGateway.get<BookResponseInterface>(`/libraries/${libraryUuid}/books/`, {
        params: {
          showAll: filters?.showAll,
          page: filters?.page,
          size: filters?.size,
        }
      });
      const books = response.data;
      return books;
    } catch (e) {
      console.log(e);
    }
  }

  static async reserveBook(request: TakeBookRequest): Promise<TakeBookResponse | string> {
    const response = await $apiGateway.post<TakeBookResponse>(`/reservations/`,
      {
        libraryUid: request.libraryUuid,
        bookUid: request.booUuid,
        tillDate: request.tillDate.format("YYYY-MM-DD"),
      }
    ).catch((error) => {
      var errorMessage: string;
      if (isAxiosError(error)) {
        if (error.response && error.response.status === 400) {
          errorMessage = `Ошибка: Эта книга в библиотеке закончилась\
            или Ваш рейтинг ниже количества Ваших бронирований`;
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
      const reservation = response.data;
      return reservation;
    }
  }

  static async getUserRating(): Promise<RatingInterface | undefined> {
    try {
      const response = await $apiGateway.get<RatingInterface>(`/rating/`);
      const rating = response.data;
      return rating;
    } catch (e) {
      console.log(e);
    }
  }

  static async getUserReservations(filters: ReservationFilter): Promise<ReservationResponseInterface | undefined> {
    try {
      const response = await $apiGateway.get<ReservationResponseInterface>(`/reservations/`, {
        params: {
          status: filters?.status,
          page: filters?.page,
          size: filters?.size,
        }
      });
      const reservations = response.data;
      return reservations;
    } catch (e) {
      console.log(e);
    }
  }

  static async returnBook(request: ReturnBook): Promise<void | string> {
    const response = await $apiGateway.post<void>(`/reservations/${request.reservationUuid}/return/`,
      {
        condition: request.condition,
        date: request.date.format("YYYY-MM-DD"),
      }
    ).catch((error) => {
      var errorMessage: string;
      if (isAxiosError(error)) {
        if (error.response && error.response.status === 400) {
          errorMessage = `${error.response.data.message}`;
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
      return;
    }
  }
}
