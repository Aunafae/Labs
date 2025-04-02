package com.example.mobapplab4;

import static android.widget.Toast.LENGTH_LONG;

import android.database.Cursor;
import android.net.ConnectivityManager;
import android.net.NetworkInfo;
import android.os.Bundle;

import androidx.activity.EdgeToEdge;
import androidx.appcompat.app.AppCompatActivity;

import android.os.Handler;
import android.os.StrictMode;
import android.util.Log;
import android.view.View;
import android.widget.TextView;
import android.widget.Toast;

import androidx.core.graphics.Insets;
import androidx.core.view.ViewCompat;
import androidx.core.view.WindowInsetsCompat;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.IOException;
import java.net.InetSocketAddress;
import java.net.Socket;
import java.net.SocketAddress;

public class MainActivity extends AppCompatActivity {
    private DataBase db;
    private NetworkURL net;
    private TextView outputTextView;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        EdgeToEdge.enable(this);
        setContentView(R.layout.activity_main);

        ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.main), (v, insets) -> {
            Insets systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars());
            v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom);
            return insets;
        });

        //this.deleteDatabase("LAB4");
        db = new DataBase(this, "LAB4");
        outputTextView = findViewById(R.id.outputTextView);
        knopkaClicked(null);

        if(!checkConnection()) {
            Toast.makeText(getApplicationContext(), "Отсутствует подключение к интернету", LENGTH_LONG).show();
        }
        else if(net == null) {
            net = new NetworkURL(this, db);
            net.execute("https://media.itmo.ru/api_get_current_song.php");
        }
    }

    public boolean checkConnection() {
        ConnectivityManager connectivityManager = (ConnectivityManager) getSystemService(CONNECTIVITY_SERVICE);
        NetworkInfo activeNetworkInfo = connectivityManager.getActiveNetworkInfo();
        if(!(activeNetworkInfo != null && activeNetworkInfo.isConnected())) return false;

        try {
            StrictMode.ThreadPolicy policy = new StrictMode.ThreadPolicy.Builder().permitAll().build();
            StrictMode.setThreadPolicy(policy);

            int timeoutMs = 3000;
            Socket sock = new Socket();
            SocketAddress sockaddr = new InetSocketAddress("oreluniver.ru", 80);
            sock.connect(sockaddr, timeoutMs);
            sock.close();
        } catch (IOException ioException) { return false; }
        return true;
    }

    public void knopkaClicked(View view){
        Cursor cursor = db.database().query("Radio", null, null, null, null, null, null);
        StringBuilder output = new StringBuilder();
        if (cursor.moveToFirst()) {
            int idIndex = cursor.getColumnIndex("id");
            int performerIndex = cursor.getColumnIndex("performer");
            int trackNameIndex = cursor.getColumnIndex("trackName");
            int timeOfInsertionIndex = cursor.getColumnIndex("timeOfInsertion");
            while (!cursor.isAfterLast()) {
                int id = cursor.getInt(idIndex);
                String performer = cursor.getString(performerIndex);
                String trackName = cursor.getString(trackNameIndex);
                String timeOfInsertion = cursor.getString(timeOfInsertionIndex);
                output.append("ID: ").append(id).append("\n")
                        .append("Performer: ").append(performer).append("\n")
                        .append("TrackName: ").append(trackName).append("\n")
                        .append("TimeOfInsertion: ").append(timeOfInsertion).append("\n\n");
                cursor.moveToNext();
            }
        }
        cursor.close();

        outputTextView.setText(output.toString());
        outputTextView.setVisibility(View.VISIBLE);

        if(!checkConnection()) {
            Toast.makeText(getApplicationContext(), "Отсутствует подключение к интернету", LENGTH_LONG).show();
        }
        else if(net == null) {
            net = new NetworkURL(this, db);
            net.execute("https://media.itmo.ru/api_get_current_song.php");
            knopkaClicked(null);
        }
    }
}