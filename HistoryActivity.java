package com.example.weatherjournal;

import androidx.appcompat.app.AppCompatActivity;
import android.database.Cursor;
import android.os.Bundle;
import android.widget.ListView;
import android.widget.SimpleCursorAdapter;
import android.widget.TextView;

import com.example.weatherjournal.data.WeatherContract;

import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.Locale;

public class HistoryActivity extends AppCompatActivity {

    private ListView historyList;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_history);

        historyList = findViewById(R.id.history_list);

        displayWeatherHistory();
    }

    private void displayWeatherHistory() {
        String[] projection = {
                WeatherContract.WeatherEntry._ID,
                WeatherContract.WeatherEntry.COLUMN_LOCATION,
                WeatherContract.WeatherEntry.COLUMN_TEMPERATURE,
                WeatherContract.WeatherEntry.COLUMN_NOTES,

        };

        Cursor cursor = getContentResolver().query(
                WeatherContract.WeatherEntry.CONTENT_URI,
                projection,
                null,
                null,
                null
        );

        String[] from = {
                WeatherContract.WeatherEntry.COLUMN_LOCATION,
                WeatherContract.WeatherEntry.COLUMN_TEMPERATURE,
                WeatherContract.WeatherEntry.COLUMN_NOTES,

        };

        int[] to = {
                R.id.text1,
                R.id.text2,
                R.id.text3,

        };

        SimpleCursorAdapter adapter = new SimpleCursorAdapter(
                this,
                R.layout.list_item_weather,
                cursor,
                from,
                to,
                0
        );

        adapter.setViewBinder(new SimpleCursorAdapter.ViewBinder() {
            @Override
            public boolean setViewValue(android.view.View view, Cursor cursor, int columnIndex) {
                if (columnIndex == cursor.getColumnIndex(WeatherContract.WeatherEntry.COLUMN_TIMESTAMP)) {
                    long timestamp = cursor.getLong(columnIndex);
                    Date date = new Date(timestamp);
                    SimpleDateFormat dateFormat = new SimpleDateFormat("dd/MM/yyyy HH:mm", Locale.getDefault());
                    String formattedDate = dateFormat.format(date);
                    ((TextView) view).setText(formattedDate);
                    return true;
                }
                return false;
            }
        });

        historyList.setAdapter(adapter);
    }
}
