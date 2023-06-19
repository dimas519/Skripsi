package com.dimas519.retrofit;




import retrofit2.Call;
import retrofit2.http.Body;
import retrofit2.http.GET;
import retrofit2.http.POST;
import retrofit2.http.Query;


public interface IRequest {
    @POST("/sensing")
    Call<String> sensing(@Body String msg);

    @GET("/interval")
    Call<String> interval(@Query("node") String node);



}
