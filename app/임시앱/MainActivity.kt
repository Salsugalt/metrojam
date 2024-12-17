package com.example.myapp

import PredictionApi
import PredictionRequest
import PredictionResponse
import android.annotation.SuppressLint
import android.os.Bundle
import android.widget.*
import androidx.appcompat.app.AppCompatActivity
import com.example.myapplication.R
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory

class MainActivity : AppCompatActivity() {

    @SuppressLint("MissingInflatedId")
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        // UI 요소
        val lineSeekBar: SeekBar = findViewById(R.id.seekBar)
        val lineTextView: TextView = findViewById(R.id.textView3)
        val timePicker: TimePicker = findViewById(R.id.timePicker)
        val timeTextView: TextView = findViewById(R.id.textView4)
        val stationEditText: EditText = findViewById(R.id.editTextText)
        val directionRadioGroup: RadioGroup = findViewById(R.id.radioGroupDirection)
        val dayTypeRadioGroup: RadioGroup = findViewById(R.id.radioGroupDayType)
        val resultTextView: TextView = findViewById(R.id.result_text)
        val resultTextView2: TextView = findViewById(R.id.result_text2)

        // Retrofit 초기화
        val retrofit = Retrofit.Builder()
            .baseUrl("http://10.0.2.2:5000") // 에뮬레이터 사용 시ip, 이외에 ipv4 사용
            .addConverterFactory(GsonConverterFactory.create())
            .build()
        val api = retrofit.create(PredictionApi::class.java)

        // 지하철 노선 SeekBar 초기화
        lineTextView.text = "지하철 노선: ${lineSeekBar.progress + 1}호선"
        lineSeekBar.setOnSeekBarChangeListener(object : SeekBar.OnSeekBarChangeListener {
            override fun onProgressChanged(seekBar: SeekBar?, progress: Int, fromUser: Boolean) {
                lineTextView.text = "지하철 노선: ${progress + 1}호선"
            }

            override fun onStartTrackingTouch(seekBar: SeekBar?) {}
            override fun onStopTrackingTouch(seekBar: SeekBar?) {}
        })

        // 24시간제로 TimePicker 설정
        timePicker.setIs24HourView(true)

        // TimePicker 초기값 설정 및 리스너
        timeTextView.text = "선택된 시간: ${timePicker.hour}시 ${timePicker.minute}분"
        timePicker.setOnTimeChangedListener { _, hour, minute ->
            val originalTime = "${hour}시${minute}분"

            // 사용자에게 반올림된 시간 표시
            timeTextView.text = "선택된 시간: $originalTime"

            /* API 호출 업데이트 */
            updateApiCall(
                api = api,
                hour = hour,
                minute = minute,
                lineSeekBar = lineSeekBar,
                stationEditText = stationEditText,
                directionRadioGroup = directionRadioGroup,
                dayTypeRadioGroup = dayTypeRadioGroup,
                resultTextView = resultTextView,
                resultTextView2 = resultTextView2
            )
        }
    }

    /* 30분 단위로 반올림하는 함수
    private fun adjustToNearest30Minutes(hour: Int, minute: Int): Pair<Int, String> {
        return if (minute < 15) {
            hour to "00"
        } else if (minute < 45) {
            hour to "30"
        } else {
            val adjustedHour = (hour + 1) % 24
            adjustedHour to "00"
        }
    }
*/
    // API 호출 함수
    private fun updateApiCall(
        api: PredictionApi,
        hour: Int,
        minute: Int,
        lineSeekBar: SeekBar,
        stationEditText: EditText,
        directionRadioGroup: RadioGroup,
        dayTypeRadioGroup: RadioGroup,
        resultTextView: TextView,
        resultTextView2: TextView
    ) {
        val line = lineSeekBar.progress + 1
        val stationName = stationEditText.text.toString()
        val direction = when (directionRadioGroup.checkedRadioButtonId) {
            R.id.rb_direction_up -> true
            R.id.rb_direction_down -> false
            else -> false
        }
        val dayType = when (dayTypeRadioGroup.checkedRadioButtonId) {
            R.id.radioButton7 -> true
            R.id.radioButton8 -> false
            else -> false
        }
        val adjustedTime = "${hour}시${minute}분"
        val request = PredictionRequest(direction, dayType, adjustedTime, stationName, line)

        api.getMedianCongestion(request).enqueue(object : Callback<PredictionResponse> {
            override fun onResponse(
                call: Call<PredictionResponse>,
                response: Response<PredictionResponse>
            ) {
                if (response.isSuccessful) {
                    response.body()?.let { result ->
                        resultTextView.text = "중앙값 혼잡도: ${result.median_congestion ?: "없음"}"
                        resultTextView2.text = "예측 혼잡도: ${result.predict_congestion ?: "없음"}"
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
