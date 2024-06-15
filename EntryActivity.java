package com.example.weatherjournal;

import androidx.appcompat.app.AppCompatActivity;
import android.content.ContentValues;
import android.net.Uri;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

import com.example.weatherjournal.data.WeatherContract;

public class EntryActivity extends AppCompatActivity {

    private TextView weatherInfo;
    private EditText entryNotes;
    private Button saveButton;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_entry);

        weatherInfo = findViewById(R.id.weather_info);
        entryNotes = findViewById(R.id.entry_notes);
        saveButton = findViewById(R.id.save_button);

        // Get weather info from MainActivity
        String weatherData = getIntent().getStringExtra("WEATHER_DATA");
        weatherInfo.setText(weatherData != null ? weatherData : "Sample Weather Info");

        saveButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                saveWeatherEntry();
            }
        });
    }

    private void saveWeatherEntry() {
        String notes = entryNotes.getText().toString();
        if (notes.isEmpty()) {
            Toast.makeText(this, "Please enter some notes", Toast.LENGTH_SHORT).show();
            return;
        }

        String weatherText = weatherInfo.getText().toString();
        String[] weatherParts = weatherText.split("\n");
        String location = weatherParts[0].replace("Location: ", "");
        String temperature = weatherParts[1].replace("Temperature: ", "").replace("°C", "");

        ContentValues values = new ContentValues();
        values.put(WeatherContract.WeatherEntry.COLUMN_LOCATION, location);
        values.put(WeatherContract.WeatherEntry.COLUMN_TEMPERATURE, temperature);
        values.put(WeatherContract.WeatherEntry.COLUMN_NOTES, notes);

        Uri newUri = getContentResolver().insert(WeatherContract.WeatherEntry.CONTENT_URI, values);
        if (newUri != null) {
            Toast.makeText(this, "Weather entry saved", Toast.LENGTH_SHORT).show();
        }
    }
}
