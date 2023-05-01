package API;

import API.retrofit.IRequest;
import API.retrofit.RetrofitAPI;
import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;

import static com.sun.tools.doclint.Entity.pi;


public class API {
    private final String endpoint;

    public API(String endpoint){
        this.endpoint=endpoint;
    }

    public String sendToServer(String msg) {
        IRequest ireq = RetrofitAPI.getRetro(this.endpoint).create(IRequest.class);
        Call<String> cl = ireq.sensing(msg);
        cl.enqueue(new Callback<String>() {
            @Override
            public void onResponse(Call<String> call, Response<String> response) {

                if (response.isSuccessful()) {
                    if (response.body() != null) {
                        System.out.println("onSuccess" + response.body().toString());
                    } else {
                        System.out.println("onEmptyResponse Returned empty response");//Toast.makeText(getContext(),"Nothing returned",Toast.LENGTH_LONG).show();
                    }
                }


            }

            @Override
            public void onFailure(Call<String> call, Throwable throwable) {

            }

        });
        return null;

    }










}
