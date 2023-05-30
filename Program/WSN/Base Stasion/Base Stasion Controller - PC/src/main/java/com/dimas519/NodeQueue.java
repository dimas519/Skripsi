package com.dimas519;

import java.util.LinkedList;
import java.util.Queue;

public class NodeQueue {
    private Long nodeAddress;
    private Queue<String> queue;

    public NodeQueue(Long nodeAddress){
        this.nodeAddress=nodeAddress;
        this.queue= new LinkedList<>();
    }

    public Long getAddress(){
        return this.nodeAddress;
    }

    public void setQueue(String msg){
        this.queue.add(msg);
    }
    public boolean emptyQueue(){
        return queue.isEmpty();
    }

    public String getQueue(){
        return queue.poll();
    }

}
