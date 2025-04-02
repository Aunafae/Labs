package com.example.mobapplab4;

import android.content.ContentValues;
import android.content.Context;
import android.database.Cursor;
import android.database.sqlite.SQLiteDatabase;
import android.database.sqlite.SQLiteOpenHelper;
import android.util.Log;

import org.json.JSONException;
import org.json.JSONObject;

import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.TimeZone;


public class DataBase extends SQLiteOpenHelper {
    private final SQLiteDatabase db;

    public DataBase(Context context, String name) {
        super(context, name, null, 1);
        db = getWritableDatabase();
    }

    @Override
    public void onCreate(SQLiteDatabase db) {
        db.execSQL("CREATE TABLE IF NOT EXISTS 'Radio'(id INTEGER PRIMARY KEY AUTOINCREMENT, performer TEXT, trackName TEXT, timeOfInsertion TEXT)");
    }

    @Override
    public void onUpgrade(SQLiteDatabase db, int oldVersion, int newVersion) {
        db.execSQL("DROP TABLE IF EXISTS 'Radio'");
        onCreate(db);
    }

    public SQLiteDatabase database() {
        return db;
    }

    private void insert(String performer, String trackName, String timeOfInsertion) {
        ContentValues values = new ContentValues();
        values.put("performer", performer);
        values.put("trackName", trackName);
        values.put("timeOfInsertion", timeOfInsertion);
        db.insert("Radio", null, values);
    }

    public boolean insertTrackIfNotExists(String track) {
        JSONObject jsonObject;
        String performer = null;
        String trackName = null;
        try {
            jsonObject = new JSONObject(track);
            performer = jsonObject.getString("info").split("-")[0];
            trackName = jsonObject.getString("info").split("-")[1];
        } catch (JSONException ignored) { return false; }
        track = performer + " - " + trackName;

        String lastTrack = getLastTrack();
        if (!track.equals(lastTrack)) {
            SimpleDateFormat date = new SimpleDateFormat("HH:mm   dd.MM.yyyy");
            date.setTimeZone(TimeZone.getTimeZone("Europe/Moscow"));
            String timeOfInsertion = date.format(new Date());
            insert(performer, trackName, timeOfInsertion);
        }
        else return false;
        return true;
    }

    private String getLastTrack() {
        String lastTrack = null;
        Cursor cursor = db.query("Radio", new String[]{"performer", "trackName"}, null, null, null, null, "id DESC", "1");
        if (cursor.moveToFirst()) {
            int performerIndex = cursor.getColumnIndex("performer");
            int trackNameIndex = cursor.getColumnIndex("trackName");
            while (!cursor.isAfterLast()) {
                String performer = cursor.getString(performerIndex);
                String trackName = cursor.getString(trackNameIndex);
                lastTrack = performer + " - " + trackName;
                cursor.moveToNext();
            }
            cursor.close();
        }
        return lastTrack;
    }
}