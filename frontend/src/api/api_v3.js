import axios from 'axios';

const api = axios.create({
  baseURL: 'http://127.0.0.1:8000/', //replace with your BaseURL
  headers: {
    'Content-Type': 'application/json', // change according header type accordingly
  },
});


api.interceptors.request.use(
    (config) => {
      const accessToken = localStorage.getItem('access_token'); // get stored access token
      if (accessToken) {
        config.headers.Authorization = `Bearer ${accessToken}`; // set in header
      }
      return config;
    },
    (error) => {
      return Promise.reject(error);
    }
  );


  api.interceptors.response.use(
    (response) => {
      return response;
    },
    async (error) => {
      const originalRequest = error.config;
      if (error.response.status === 401 && !originalRequest._retry) {
        originalRequest._retry = true;
        const refreshToken = localStorage.getItem('refresh_token');
        if (refreshToken) {
          try {
            const response = await axios.post(`${BASE_URL}/auth/token/refresh/`, {refresh: refreshToken});
            // don't use axious instance that already configured for refresh token api call
            const newAccessToken = response.data.accessToken;
            localStorage.setItem('access_token', newAccessToken);  //set new access token
            originalRequest.headers.Authorization = `Bearer ${newAccessToken}`;
            return axios(originalRequest); //recall Api with new token
          } catch (error) {
            // Handle token refresh failure
            // mostly logout the user and re-authenticate by login again
          }
        }
      }
      return Promise.reject(error);
    }
  );


export default api;