package com.example.weatherjournal.data;

import android.content.ContentResolver;
import android.net.Uri;
import android.provider.BaseColumns;

public class WeatherContract {
    public static final String CONTENT_AUTHORITY = "com.example.weatherjournal";
    public static final Uri BASE_CONTENT_URI = Uri.parse("content://" + CONTENT_AUTHORITY);
    public static final String PATH_WEATHER = "weather";

    public static final class WeatherEntry implements BaseColumns {
        public static final Uri CONTENT_URI = Uri.withAppendedPath(BASE_CONTENT_URI, PATH_WEATHER);

        public static final String TABLE_NAME = "weather";
        public static final String COLUMN_LOCATION = "location";
        public static final String COLUMN_TEMPERATURE = "temperature";
        public static final String COLUMN_DESCRIPTION = "description";
        public static final String COLUMN_TIMESTAMP = "timestamp";
        public static final String COLUMN_NOTES = "notes";

        public static final String _ID = BaseColumns._ID;

        // MIME type for a list of weather entries
        public static final String CONTENT_LIST_TYPE =
                ContentResolver.CURSOR_DIR_BASE_TYPE + "/" + CONTENT_AUTHORITY + "/" + PATH_WEATHER;

        // MIME type for a single weather entry
        public static final String CONTENT_ITEM_TYPE =
                ContentResolver.CURSOR_ITEM_BASE_TYPE + "/" + CONTENT_AUTHORITY + "/" + PATH_WEATHER;
    }
}
