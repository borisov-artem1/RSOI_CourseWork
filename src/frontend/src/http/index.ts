import axios, { AxiosResponse, InternalAxiosRequestConfig } from "axios";
import settings from "../settings";
import { AuthResponse } from "../model/response/auth.response";

const ACCESS_TOKEN = `accessToken`;
const REFRESH_TOKEN = `refreshToken`;

export const AUTH_API_URL = `
  http://`+
  `${settings.userService.host}:`+
  `${settings.userService.port}/`+
  `api/v1/`;
export const USER_API_URL = `
  http://`+
  `${settings.userService.host}:`+
  `${settings.userService.port}/`+
  `api/v1/`; // для логики своей захотел их разделить, хоть они и одинаковые
export const GATEWAY_API_URL = `
  http://`+
  `${settings.gatewayService.host}:`+
  `${settings.gatewayService.port}/`+
  `api/v1/`;
export const STATISTICS_API_URL = `
  http://`+
  `${settings.statisticsService.host}:`+
  `${settings.statisticsService.port}/`+
  `api/v1/`;

// AUTH
export const $apiAuth = axios.create({
  baseURL: AUTH_API_URL,
});
// AUTH

// USER
export const $apiUser = axios.create({
  baseURL: USER_API_URL,
});

$apiUser.interceptors.request.use((config: InternalAxiosRequestConfig) => {
  config.headers.Authorization = `Bearer ${localStorage.getItem(ACCESS_TOKEN)}`;
  return config;
});

$apiUser.interceptors.response.use((config: AxiosResponse) => {
  return config;
}, (async (error) => {
  const originalRequest = error.config;
  if (error.response.status === 401 && error.config && !error.config._isRetry) {
    originalRequest._isRetry = true;
    try {
      const data = {
        "refresh_token": localStorage.getItem(REFRESH_TOKEN),
      };
      const response = await $apiAuth.post<AuthResponse>(`/user/refresh/`, data).catch(_ => {
        localStorage.clear();
      });
      
      if (response) {
        localStorage.setItem(ACCESS_TOKEN, response.data.access_token as string);
        return $apiUser.request(originalRequest);
      }
    } catch (e) {
      console.log(e);
    }
  }
  throw error;
}));
// USER

// GATEWAY
export const $apiGateway = axios.create({
  baseURL: GATEWAY_API_URL,
});

$apiGateway.interceptors.request.use((config: InternalAxiosRequestConfig) => {
  config.headers.Authorization = `Bearer ${localStorage.getItem(ACCESS_TOKEN)}`;
  return config;
});

$apiGateway.interceptors.response.use((config: AxiosResponse) => {
  return config;
}, (async (error) => {
  const originalRequest = error.config;
  if (error.response.status === 401 && error.config && !error.config._isRetry) {
    originalRequest._isRetry = true;
    try {
      const data = {
        "refresh_token": localStorage.getItem(REFRESH_TOKEN),
      };
      const response = await $apiAuth.post<AuthResponse>(`/user/refresh/`, data).catch(_ => {
        localStorage.clear();
      });

      if (response) {
        localStorage.setItem(ACCESS_TOKEN, response.data.access_token as string);
        return $apiGateway.request(originalRequest);
      }
    } catch (e) {
      console.log(e);
    }
  }
  throw error;
}));
// GATEWAY


// STATISTICS
export const $apiStatistics = axios.create({
  baseURL: STATISTICS_API_URL,
});

$apiStatistics.interceptors.request.use((config: InternalAxiosRequestConfig) => {
  config.headers.Authorization = `Bearer ${localStorage.getItem(ACCESS_TOKEN)}`;
  return config;
});

$apiStatistics.interceptors.response.use((config: AxiosResponse) => {
  return config;
}, (async (error) => {
  const originalRequest = error.config;
  if (error.response.status === 401 && error.config && !error.config._isRetry) {
    originalRequest._isRetry = true;
    try {
      const data = {
        "refresh_token": localStorage.getItem(REFRESH_TOKEN),
      };
      const response = await $apiAuth.post<AuthResponse>(`/user/refresh/`, data).catch(_ => {
        localStorage.clear();
      });

      if (response) {
        localStorage.setItem(ACCESS_TOKEN, response.data.access_token as string);
        return $apiStatistics.request(originalRequest);
      }
    } catch (e) {
      console.log(e);
    }
  }
  throw error;
}));
// STATISTICS


// export const LIBRARY_API_URL = `
//   http://`+
//   `${settings.libraryService.host}:`+
//   `${settings.libraryService.port}/`+
//   `api/v1/`;
// export const RATING_API_URL = `
//   http://`+
//   `${settings.ratingService.host}:`+
//   `${settings.ratingService.port}/`+
//   `api/v1/`;
// export const RESERVATION_API_URL = `
//   http://`+
//   `${settings.reservationService.host}:`+
//   `${settings.reservationService.port}/`+
//   `api/v1/`;

// // LIBRARY
// export const $apiLibrary = axios.create({
//   baseURL: LIBRARY_API_URL,
// });

// $apiLibrary.interceptors.request.use((config: InternalAxiosRequestConfig) => {
//   config.headers.Authorization = `Bearer ${localStorage.getItem(ACCESS_TOKEN)}`;
//   return config;
// });

// $apiLibrary.interceptors.response.use((config: AxiosResponse) => {
//   return config;
// }, (async (error) => {
//   const originalRequest = error.config;
//   if (error.response.status === 401 && error.config && !error.config._isRetry) {
//     originalRequest._isRetry = true;
//     try {
//       const data = {
//         "refresh_token": localStorage.getItem(REFRESH_TOKEN),
//       };
//       const response = await $apiAuth.post<AuthResponse>(`/user/refresh/`, data);
//       localStorage.setItem(ACCESS_TOKEN, response.data.access_token as string);
//       return $apiLibrary.request(originalRequest);
//     } catch (e) {
//       console.log(e);
//     }
//   }
//   throw error;
// }));
// // LIBRARY

// // RATING
// export const $apiRating = axios.create({
//   baseURL: RATING_API_URL,
// });

// $apiRating.interceptors.request.use((config: InternalAxiosRequestConfig) => {
//   config.headers.Authorization = `Bearer ${localStorage.getItem(ACCESS_TOKEN)}`;
//   return config;
// });

// $apiRating.interceptors.response.use((config: AxiosResponse) => {
//   return config;
// }, (async (error) => {
//   const originalRequest = error.config;
//   if (error.response.status === 401 && error.config && !error.config._isRetry) {
//     originalRequest._isRetry = true;
//     try {
//       const data = {
//         "refresh_token": localStorage.getItem(REFRESH_TOKEN),
//       };
//       const response = await $apiAuth.post<AuthResponse>(`/user/refresh/`, data);
//       localStorage.setItem(ACCESS_TOKEN, response.data.access_token as string);
//       return $apiRating.request(originalRequest);
//     } catch (e) {
//       console.log(e);
//     }
//   }
//   throw error;
// }));
// // RATING

// // RESERVATION
// export const $apiReservation = axios.create({
//   baseURL: RESERVATION_API_URL,
// });

// $apiReservation.interceptors.request.use((config: InternalAxiosRequestConfig) => {
//   config.headers.Authorization = `Bearer ${localStorage.getItem(ACCESS_TOKEN)}`;
//   return config;
// });

// $apiReservation.interceptors.response.use((config: AxiosResponse) => {
//   return config;
// }, (async (error) => {
//   const originalRequest = error.config;
//   if (error.response.status === 401 && error.config && !error.config._isRetry) {
//     originalRequest._isRetry = true;
//     try {
//       const data = {
//         "refresh_token": localStorage.getItem(REFRESH_TOKEN),
//       };
//       const response = await $apiAuth.post<AuthResponse>(`/user/refresh/`, data);
//       localStorage.setItem(ACCESS_TOKEN, response.data.access_token as string);
//       return $apiReservation.request(originalRequest);
//     } catch (e) {
//       console.log(e);
//     }
//   }
//   throw error;
// }));
// // RESERVATION
