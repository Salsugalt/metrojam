package com.example.myapp

import PredictionApi
import PredictionRequest
import PredictionResponse
import android.os.Bundle
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity
import com.example.myapplication.R
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response

class MainActivity : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        // Retrofit 초기화
        val retrofit = Retrofit.Builder()
            .baseUrl("http://10.0.2.2:5000") // 에뮬레이터 사용 시 //http://10.0.2.2:5000 //http://172.28.0.12:5000 //ipv4 ip 입력
            .addConverterFactory(GsonConverterFactory.create())
            .build()

        // API 인터페이스 생성
        val api = retrofit.create(PredictionApi::class.java)

        // 요청 데이터
        val request = PredictionRequest(
            direction = true,
            day_type = true,
            time = "12시00분",
            station_name = "서울역",
            line = 1
        )

        // 결과를 표시할 TextView
        val resultTextView: TextView = findViewById(R.id.result_text)

        // API 호출
        api.getMedianCongestion(request).enqueue(object : Callback<PredictionResponse> {
            override fun onResponse(call: Call<PredictionResponse>, response: Response<PredictionResponse>) {
                if (response.isSuccessful) {
                    val result = response.body()
                    if (result?.median_congestion != null) {
                        resultTextView.text = "혼잡률: ${result.median_congestion}"
                    } else {
                        resultTextView.text = "오류: ${result?.error}"
                    }
                } else {
                    resultTextView.text = "서버 오류: ${response.code()}"
                }
            }

            override fun onFailure(call: Call<PredictionResponse>, t: Throwable) {
                resultTextView.text = "네트워크 오류: ${t.message}"
            }
        })
    }
}
