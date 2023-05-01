package API.retrofit;




import retrofit2.Call;
import retrofit2.Response;
import retrofit2.http.Body;

import retrofit2.http.POST;


public interface IRequest {
    @POST("/sensing")
    public Call<String> sensing(@Body String x);





}
