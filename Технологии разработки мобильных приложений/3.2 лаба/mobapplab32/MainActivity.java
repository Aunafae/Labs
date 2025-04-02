package com.example.mobapplab32;

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
        SQLiteOpenHelper help = new SQLiteOpenHelper(this, "LAB", null, 2) {
            @Override
            public void onCreate(SQLiteDatabase db) {
                db.execSQL("CREATE TABLE IF NOT EXISTS 'Одногруппники'(id INTEGER PRIMARY KEY AUTOINCREMENT, f TEXT, i TEXT, o TEXT, date_time TEXT)");
            }

            @Override
            public void onUpgrade(SQLiteDatabase db, int oldVersion, int newVersion) {
                db.execSQL("DROP TABLE IF EXISTS 'Одногруппники'");
                onCreate(db);
            }
        };
        db = help.getWritableDatabase();
        db.delete("Одногруппники", null, null);
        insert("Банных", "Мария", "Алексеевна");
        insert("Мельников", "Артем", "Евгеньевич");
        insert("Дорофеева", "Анна", "Вадимовна");
        insert("Василения", "Иван", "Валерьевич");
        insert("Тимаков", "Павел", "Евгеньевич");
    }

    private void insert(String f, String i, String o){
        ContentValues values = new ContentValues();
        String date_time = getCurrentDateTime();
        values.put("f", f);
        values.put("i", i);
        values.put("o", o);
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
            int fIndex = cursor.getColumnIndex("f");
            int iIndex = cursor.getColumnIndex("i");
            int oIndex = cursor.getColumnIndex("o");
            int dateTimeIndex = cursor.getColumnIndex("date_time");
            while (!cursor.isAfterLast()) {
                int id = cursor.getInt(idIndex);
                String f = cursor.getString(fIndex);
                String i = cursor.getString(iIndex);
                String o = cursor.getString(oIndex);
                String dateTime = cursor.getString(dateTimeIndex);
                output.append("ID: ").append(id).append("\n")
                        .append("F: ").append(f).append("\n")
                        .append("I: ").append(i).append("\n")
                        .append("O: ").append(o).append("\n")
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
        insert("Фамилия", "Имя", "Отчество");
        Toast.makeText(this, "Запись добавлена", Toast.LENGTH_SHORT).show();
    }

    public void edit(View view){
        Cursor cursor = db.query("Одногруппники", new String[]{"id"}, null, null,null,null,null,null);

        if (cursor.moveToLast()) {
            int idIndex = cursor.getColumnIndex("id");
            int id = cursor.getInt(idIndex);
            ContentValues values = new ContentValues();
            values.put("f", "Иванов");
            values.put("i", "Иван");
            values.put("o", "Иванович");
            db.update("Одногруппники", values, "id = ?", new String[]{String.valueOf(id)});
            Toast.makeText(this, "Запись обновлена", Toast.LENGTH_SHORT).show();
        }
        cursor.close();
    }
}