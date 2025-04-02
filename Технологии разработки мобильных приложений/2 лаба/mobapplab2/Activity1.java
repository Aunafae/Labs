package com.example.mobapplab2;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;

import androidx.activity.EdgeToEdge;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.graphics.Insets;
import androidx.core.view.ViewCompat;
import androidx.core.view.WindowInsetsCompat;

public class Activity1 extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        EdgeToEdge.enable(this);
        setContentView(R.layout.activity_1);
        ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.main), (v, insets) -> {
            Insets systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars());
            v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom);
            return insets;
        });
    }

    public void to_activity_2(View view){
        Intent intent = new Intent(this, Activity2.class);
        startActivity(intent);
    }
    public void to_activity_3(View view){
        Intent intent = new Intent(this, Activity3.class);
        startActivity(intent);
    }
    public void to_activity_4(View view){
        Intent intent = new Intent(this, Activity4.class);
        startActivity(intent);
    }
    public void exit(View view){
        finishAndRemoveTask();
    }
}