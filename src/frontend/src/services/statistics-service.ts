import {$apiStatistics} from "../http";
import { StatisticsResponseInterface, StatisticsFilter } from "../model/interface/statistics.interface";

export default class StatisticsService {
  static async getStatistics(filters?: StatisticsFilter): Promise<StatisticsResponseInterface | undefined> {
    try {
      const response = await $apiStatistics.get<StatisticsResponseInterface>('/statistics/', {
        params: {
          page: filters?.page,
          size: filters?.size,
        }
      });
      const statistics = response.data;
      return statistics;
    } catch (e) {
      console.log(e);
    }
  }
}
