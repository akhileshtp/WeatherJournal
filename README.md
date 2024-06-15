# WeatherJournal
**Overview**
The Weather Journal App is an Android application that allows users to fetch current weather data for a specified location and record personal notes about the weather. The app displays real-time weather information and stores weather entries with timestamps and user notes. Users can view their history of weather entries and manage their weather journal.

**Features**
Real-time Weather Data: Fetches current weather information using the OpenWeatherMap API.
Weather Entry Recording: Users can add entries with weather details and personal notes.
Weather History: Displays a list of all recorded weather entries.
User-friendly Interface: Easy navigation with buttons to add new entries and view history.
**Installation**
Clone the repository.
**Usage**
Fetch Weather Data: On launching the app, it automatically fetches weather data for a default location (Kannur). The weather information is displayed on the main screen.

Add a Weather Entry: Click the "Add Entry" button to navigate to the entry screen. Here, you can view the current weather details and add personal notes. Save the entry to record it.

View History: Click the "View History" button to see a list of all recorded weather entries, including the location, temperature, notes, and timestamp.

**Code Structure**
MainActivity.java: Handles fetching and displaying real-time weather data.
EntryActivity.java: Manages adding new weather entries with user notes.
HistoryActivity.java: Displays a list of all weather entries stored in the database.
WeatherContract.java: Defines the schema and contract for the SQLite database.
WeatherProvider.java: Manages CRUD operations for the weather data.
Database
The app uses an SQLite database to store weather entries. Each entry includes the following fields:

location (String): The location for which the weather data is recorded.
temperature (float): The recorded temperature.
notes (String): User notes about the weather.
timestamp (long): The time when the entry was recorded.

**Acknowledgements**
OpenWeatherMap API for providing the weather data.
Coursera for Android lessons.
