package com.example.weatherjournal.network;

import com.google.gson.annotations.SerializedName;

public class WeatherResponse {

    @SerializedName("main")
    public Main main;

    @SerializedName("name")
    public String name;

    public class Main {
        @SerializedName("temp")
        public float temp;
    }
}
