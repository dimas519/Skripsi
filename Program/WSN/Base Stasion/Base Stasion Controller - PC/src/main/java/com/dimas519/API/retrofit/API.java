package com.dimas519.API.retrofit;

import com.dimas519.API.BaseStasionControllerInterface;
import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;



public class API {
    private final String endpoint;
    private final BaseStasionControllerInterface baseInterface;


    public API(String endpoint, BaseStasionControllerInterface bsInterface){
        this.baseInterface=bsInterface;
        this.endpoint=endpoint;
    }

    public void sendToServer(String source,String msg) {

        IRequest ireq = RetrofitAPI.getRetro(this.endpoint).create(IRequest.class);
        Call<String> cl = ireq.sensing(msg);

        cl.enqueue(new Callback<String>() {
            @Override
            public void onResponse(Call<String> call, Response<String> response) {

                if (response.isSuccessful()) {
                    if (response.body() != null) {
                        String resp=response.body();
                        baseInterface.setApiResponse(source,resp);
                    } else {
                        System.out.println("fail");
                    }
                }


            }

            @Override
            public void onFailure(Call<String> call, Throwable throwable) {
                System.out.println("fail2");
            }

        });
    }










}
