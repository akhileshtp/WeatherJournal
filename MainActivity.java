package com.example.weatherjournal;

import androidx.appcompat.app.AppCompatActivity;
import android.content.ContentValues;
import android.content.Intent;
import android.net.Uri;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;

import com.example.weatherjournal.data.WeatherContract;
import com.example.weatherjournal.network.ApiClient;
import com.example.weatherjournal.network.WeatherResponse;
import com.example.weatherjournal.network.WeatherService;

import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;

public class MainActivity extends AppCompatActivity {

    private TextView weatherInfo;
    private Button addEntryButton;
    private Button viewHistoryButton;

    private static final String API_KEY = "f7d698b9786f2e93298eac5fa71d2c8d"; // Replace with your OpenWeatherMap API key

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        weatherInfo = findViewById(R.id.weather_info);
        addEntryButton = findViewById(R.id.add_entry_button);
        viewHistoryButton = findViewById(R.id.view_history_button);

        addEntryButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent intent = new Intent(MainActivity.this, EntryActivity.class);
                String weatherText = weatherInfo.getText().toString();
                intent.putExtra("WEATHER_DATA", weatherText);
                startActivity(intent);
            }
        });

        viewHistoryButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent intent = new Intent(MainActivity.this, HistoryActivity.class);
                startActivity(intent);
            }
        });

        // Initially fetch weather data on app startup
        fetchWeatherData("Kannur");
    }

    private void fetchWeatherData(String location) {
        WeatherService weatherService = ApiClient.getClient().create(WeatherService.class);
        Call<WeatherResponse> call = weatherService.getCurrentWeather(location, API_KEY);
        call.enqueue(new Callback<WeatherResponse>() {
            @Override
            public void onResponse(Call<WeatherResponse> call, Response<WeatherResponse> response) {
                if (response.isSuccessful()) {
                    WeatherResponse weatherResponse = response.body();
                    double tempInKelvin = weatherResponse.main.temp;
                    double tempInCelsius = tempInKelvin - 273.15;
                    String weatherText = "Location: " + weatherResponse.name + "\n"
                            + "Temperature: " + String.format("%.2f", tempInCelsius) + "°C";
                    weatherInfo.setText(weatherText);
                } else {
                    Log.e("MainActivity", "Response not successful: " + response.errorBody());
                    Toast.makeText(MainActivity.this, "Failed to fetch weather data", Toast.LENGTH_SHORT).show();
                }
            }

            @Override
            public void onFailure(Call<WeatherResponse> call, Throwable t) {
                Log.e("MainActivity", "Error fetching weather data", t);
                Toast.makeText(MainActivity.this, "Failed to fetch weather data", Toast.LENGTH_SHORT).show();
            }
        });
    }

    private void saveWeatherData(String notes) {
        String weatherText = weatherInfo.getText().toString();
        if (weatherText.isEmpty()) {
            Toast.makeText(this, "No weather data to save", Toast.LENGTH_SHORT).show();
            return;
        }

        String[] weatherParts = weatherText.split("\n");
        String location = weatherParts[0].replace("Location: ", "");
        String temperature = weatherParts[1].replace("Temperature: ", "").replace("°C", "");

        ContentValues values = new ContentValues();
        values.put(WeatherContract.WeatherEntry.COLUMN_LOCATION, location);
        values.put(WeatherContract.WeatherEntry.COLUMN_TEMPERATURE, temperature);
        values.put(WeatherContract.WeatherEntry.COLUMN_NOTES, notes);

        Uri uri = getContentResolver().insert(WeatherContract.WeatherEntry.CONTENT_URI, values);
        if (uri != null) {
            Toast.makeText(this, "Weather data saved", Toast.LENGTH_SHORT).show();
        }
    }
}
