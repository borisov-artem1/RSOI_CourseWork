export interface StatisticsInterface {
  id: number;
  method: string;
  url: string;
  status_code: number;
  time: string;
}

export interface StatisticsResponseInterface {
  items: StatisticsInterface[];
  page: number;
  pageSize: number;
  totalElements: number;
}

export interface StatisticsFilter {
  page?: number;
  size?: number;
}
