import { BookInterface } from "../interface/book.interface";
import { LibraryInterface } from "../interface/library.interface";
import { RatingInterface } from "../interface/rating.interface";

export interface TakeBookResponse {
  reservationUid: string;
  status: "RENTED" | "RETURNED" | "EXPIRED";
  startDate: string;
  tillDate: string;
  library: LibraryInterface;
  book: BookInterface;
  rating: RatingInterface;
}
