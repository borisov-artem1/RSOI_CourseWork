import { ServiceSettings } from "./types"

class Settings {
  public userService: ServiceSettings = {
    host: "51.250.38.163",
    port: 8888,
  }

  public gatewayService: ServiceSettings = {
    host: "51.250.38.163",
    port: 8080,
  }

  public statisticsService: ServiceSettings = {
    host: "51.250.38.163",
    port: 8090,
  }

  public defaultPageSize: number = 5;
  public defaultStatisticsPageSize: number = 50;
}

const settings = new Settings();

export default settings;

// public libraryService: ServiceSettings = {
//   host: "",
//   port: 1111,
// }

// public ratingService: ServiceSettings = {
//   host: "",
//   port: 1111,
// }

// public reservationService: ServiceSettings = {
//   host: "",
//   port: 1111,
// }
