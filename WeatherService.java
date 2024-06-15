package com.example.weatherjournal.network;

import com.example.weatherjournal.network.WeatherResponse;
import retrofit2.Call;
import retrofit2.http.GET;
import retrofit2.http.Query;

public interface WeatherService {
    @GET("weather")
    Call<WeatherResponse> getCurrentWeather(
            @Query("q") String location,
            @Query("appid") String apiKey
    );
}
