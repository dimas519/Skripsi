package com.dimas519.retrofit;


import com.dimas519.NodeQueue;

import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;
import java.util.List;


public class API {
    private final String endPoint;
    private List<NodeQueue> queueNode;


    public API(String endPoint, List<NodeQueue> queueNode){

        this.endPoint=endPoint;
        this.queueNode=queueNode;
    }

    public void sendToServer(String source,String msg,boolean sensing) {
        System.out.println("TO API "+msg);
        IRequest ireq = RetrofitAPI.getRetro(this.endPoint).create(IRequest.class);
        Call<String> cl;
        if(sensing) {
            cl = ireq.sensing(msg);
        }else{
            cl=ireq.interval(msg);
        }

        cl.enqueue(new Callback<String>() {
            @Override
            public void onResponse(Call<String> call, Response<String> response) {

                if (response.isSuccessful()) {
                    if (response.body() != null) {
                        String responseString=response.body();
                        Long addressNS=Long.parseLong(source);
                        System.out.println("FROM API "+responseString);

                        if(responseString.equals("{\"result\":false}")|| responseString.equals("{\"result\":true}")){
                        //do nothing karena dia tidak termasuk kedalam re-config node sensor

                        }else{
                            boolean addSensor=false;
                            for (NodeQueue currQueue: queueNode){
                                if(currQueue.getAddress()==addressNS){
                                    currQueue.setQueue(responseString);
                                    addSensor=true;
                                    break;
                                }
                            }
                            if(!addSensor){
                                NodeQueue newSensor=new NodeQueue(addressNS);
                                newSensor.setQueue(responseString);
                                queueNode.add(newSensor);
                            }
                        }



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
