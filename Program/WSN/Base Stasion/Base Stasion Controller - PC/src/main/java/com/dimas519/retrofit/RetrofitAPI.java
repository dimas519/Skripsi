package com.dimas519.retrofit;




import retrofit2.Retrofit;

import retrofit2.converter.scalars.ScalarsConverterFactory;

public class RetrofitAPI{
    public static Retrofit getRetro(String API_url ) {
//        Gson gson= new GsonBuilder().setLenient().create();
        Retrofit ret=new Retrofit.Builder()
                .baseUrl(API_url)
                .addConverterFactory(ScalarsConverterFactory.create())
//                .addConverterFactory(GsonConverterFactory.create(gson))
                .build();
        return ret;
    }

}
