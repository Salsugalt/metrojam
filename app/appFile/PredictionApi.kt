import retrofit2.Call
import retrofit2.http.Body
import retrofit2.http.POST

data class PredictionRequest(
    val direction: Boolean,
    val day_type: Boolean,
    val time: String,
    val station_name: String,
    val line: Int
)

data class PredictionResponse(
    val median_congestion: Double?,
    val error: String?
)

interface PredictionApi {
    @POST("/predict")
    fun getMedianCongestion(@Body request: PredictionRequest): Call<PredictionResponse>
}
