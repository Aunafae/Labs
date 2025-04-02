package com.example.mobapplab4;

import android.database.Cursor;
import android.os.AsyncTask;
import android.util.Log;
import android.view.View;

import java.io.BufferedInputStream;
import java.io.InputStream;
import java.net.URL;
import java.net.URLEncoder;
import java.nio.charset.StandardCharsets;
import java.util.Arrays;

import javax.net.ssl.HttpsURLConnection;

public class NetworkURL extends AsyncTask<String, Integer, Void> {
    URL url;
    private DataBase db;
    MainActivity app;

    NetworkURL(MainActivity app, DataBase db) {
        this.db = db;
        this.app = app;
    }

    private String getTrack(String url_addr){
        String track = null;
        if(!app.checkConnection()) return null;
        try {
            url = new URL(url_addr);

            HttpsURLConnection connection = (HttpsURLConnection) url.openConnection();
            connection.setConnectTimeout(3000);

            String res = URLEncoder.encode("login", "UTF-8")+"="+URLEncoder.encode("4707login", "UTF-8")+
                    "&"+URLEncoder.encode("password", "UTF-8")+"="+URLEncoder.encode("4707pass", "UTF-8");

            byte[] resBytes = res.getBytes(StandardCharsets.UTF_8);

            connection.setRequestMethod("POST");
            connection.setRequestProperty("Content-Type", "application/x-www-form-urlencoded");
            connection.setRequestProperty("Content-Length", String.valueOf(resBytes.length));
            connection.setDoOutput(true);

            connection.getOutputStream().write(resBytes);

            InputStream in = new BufferedInputStream(connection.getInputStream());

            int i = 0;
            byte[] buf = new byte[4096];
            int inpByte;
            while((inpByte = in.read()) != -1) {
                buf[i++] = (byte)inpByte;
            }
            String response = new String(Arrays.copyOfRange(buf, 0, i), StandardCharsets.UTF_8);

            track = response;
        } catch (Exception e) {
            Log.e("ERROR", e.toString());
        }
        return track;
    }

    @Override
    protected void onProgressUpdate(Integer... values) {
        super.onProgressUpdate(values);
        app.knopkaClicked(null);
    }

    protected Void doInBackground(String... url_addr) {
        while(true) {
            String track = getTrack(url_addr[0]);
            if(track != null) {
                if(db.insertTrackIfNotExists(track)){
                    publishProgress();
                }
                Log.e("getTrack", track);
            }
            try {
                Thread.sleep(20000);
            }
            catch (InterruptedException ignored) {}
        }
    }
}
