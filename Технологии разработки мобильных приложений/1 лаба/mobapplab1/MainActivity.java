package com.example.mobapplab1;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import androidx.appcompat.app.AppCompatActivity;

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
    }

    public void sendMessage(View view){
        Intent intent = new Intent(this, MessageActivity.class);
        String message = "Банных, Мельников";
        // первый параметр - ключ, второй - значение
        intent.putExtra("message", message);
        startActivity(intent);
    }
}