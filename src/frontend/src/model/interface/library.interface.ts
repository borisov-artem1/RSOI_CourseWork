export interface LibraryInterface {
  libraryUid: string;
  name: string;
  city: string;
  address: string;
}

export interface LibraryResponseInterface {
  items: LibraryInterface[];
  page: number;
  pageSize: number;
  totalElements: number;
}

export interface LibraryFilter {
  city?: string;
  page?: number;
  size?: number;
}
