package com.example.mobapplab3;

import android.database.sqlite.SQLiteDatabase;
import android.database.Cursor;
import android.database.sqlite.SQLiteOpenHelper;
import android.os.Bundle;

import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.Locale;

import android.widget.Toast;
import androidx.activity.EdgeToEdge;
import androidx.appcompat.app.AppCompatActivity;
import android.content.ContentValues;
import android.view.View;
import android.content.Intent;

import androidx.core.graphics.Insets;
import androidx.core.view.ViewCompat;
import androidx.core.view.WindowInsetsCompat;

public class MainActivity extends AppCompatActivity {

    private SQLiteDatabase db;
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
        this.deleteDatabase("LAB3.db");
        SQLiteOpenHelper help = new SQLiteOpenHelper(this, "LAB", null, 1) {
            @Override
            public void onCreate(SQLiteDatabase db) {
                db.execSQL("CREATE TABLE IF NOT EXISTS 'Одногруппники'(id INTEGER PRIMARY KEY AUTOINCREMENT, fio TEXT, date_time TEXT)");
            }

            @Override
            public void onUpgrade(SQLiteDatabase db, int oldVersion, int newVersion) {
                db.execSQL("DROP TABLE IF EXISTS 'Одногруппники'");
                onCreate(db);
            }
        };
        db = help.getWritableDatabase();
        db.delete("Одногруппники", null, null);
        insert("Банных Мария Алексеевна");
        insert("Мельников Артем Евгеньевич");
        insert("Дорофеева Анна Вадимовна");
        insert("Василения Иван Валерьевич");
        insert("Тимаков Павел Евгеньевич");
    }

    private void insert(String fio){
        ContentValues values = new ContentValues();
        String date_time = getCurrentDateTime();
        values.put("fio", fio);
        values.put("date_time", date_time);
        db.insert("Одногруппники", null, values);
    }
    private String getCurrentDateTime() {
        SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss", Locale.getDefault());
        return sdf.format(new Date());
    }

    public void to_activity_output(View view){
        Cursor cursor = db.query("Одногруппники", null, null, null, null, null, null);
        StringBuilder output = new StringBuilder();
        if (cursor.moveToFirst()) {
            int idIndex = cursor.getColumnIndex("id");
            int fioIndex = cursor.getColumnIndex("fio");
            int dateTimeIndex = cursor.getColumnIndex("date_time");
            while (!cursor.isAfterLast()) {
                int id = cursor.getInt(idIndex);
                String fio = cursor.getString(fioIndex);
                String dateTime = cursor.getString(dateTimeIndex);
                output.append("ID: ").append(id).append("\n")
                        .append("FIO: ").append(fio).append("\n")
                        .append("Date: ").append(dateTime).append("\n\n");
                cursor.moveToNext();
            }
        }
        cursor.close();

        Intent intent = new Intent(this, Output_activity.class);
        intent.putExtra("data", output.toString());
        startActivity(intent);
    }

    public void add(View view){
        insert("Фамилия Имя Отчество");
        Toast.makeText(this, "Запись добавлена", Toast.LENGTH_SHORT).show();
    }

    public void edit(View view){
        Cursor cursor = db.query("Одногруппники", new String[]{"id"}, null, null,null,null,null,null);

        if (cursor.moveToLast()) {
            int idIndex = cursor.getColumnIndex("id");
            int id = cursor.getInt(idIndex);
            ContentValues values = new ContentValues();
            values.put("fio", "Иванов Иван Иванович");
            db.update("Одногруппники", values, "id = ?", new String[]{String.valueOf(id)});
            Toast.makeText(this, "Запись обновлена", Toast.LENGTH_SHORT).show();
        }
        cursor.close();
    }
}