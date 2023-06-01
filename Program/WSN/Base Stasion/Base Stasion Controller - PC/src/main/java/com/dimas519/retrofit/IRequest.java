package com.dimas519.retrofit;




import retrofit2.Call;
import retrofit2.http.Body;
import retrofit2.http.POST;

public interface IRequest {
    @POST("/sensing")
    Call<String> sensing(@Body String x);

    @POST("/interval")
    Call<String> interval(@Body String x);




}
