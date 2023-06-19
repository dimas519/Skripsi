package com.dimas519;


import com.dimas519.retrofit.API;
import org.apache.tools.ant.BuildException;
import org.apache.tools.ant.DefaultLogger;
import org.apache.tools.ant.Project;
import org.apache.tools.ant.ProjectHelper;

import java.io.*;
import java.util.ArrayList;
import java.util.List;

import com.virtenio.commander.toolsets.preon32.Preon32Helper;
import com.virtenio.commander.io.DataConnection;
import purejavacomm.PureJavaIllegalStateException;

/**
 * args pada kelas ini
 *  0 : path ke buildUser.xml
 *  1 : path ke build.xml
 *  2 : port number to preon  //sesuaikan dengan yang di context 1
 *  3 : API endpoint
 */

public class BaseStationControllerUSART {

    private API myApi;
    private  Preon32Helper nodeHelper;
    private DataConnection dataConnection;
    private BufferedInputStream bufferedInputStream;
    private volatile boolean writing=false;
    List<NodeQueue> queueNode;

    private String[] args;
    public BaseStationControllerUSART(String[] args){
        this.executeAtPreon("buildUser.xml","context.set.1");//ubah ke context 1, atau context yg berisikan ant build untuk preon
        this.args=args;


        try{
            this.executeAtPreon("build.xml","cmd.time.synchronize"); //time sync karena preon punya rtc tapi tidak ada battery untuk rtc jalan

        }catch(BuildException e){
            System.err.print("com to preon problem with msg:"+e.getMessage());
        }


        try {
            this.nodeHelper = new Preon32Helper(args[1],115200);
            this.dataConnection = this.nodeHelper.runModule(args[2]);
            bufferedInputStream = new BufferedInputStream(this.dataConnection.getInputStream());

        } catch (Exception e) {
            System.out.println("failed open connection to preon32"+e.getMessage());
        }

        this.queueNode=new ArrayList<>();
        this.myApi=new API(args[0],this.queueNode);

        this.runBaseStasionPC();
    }

    private void runBaseStasionPC(){
        System.out.println("System ready to use");
        


        while(!false){
            try {

                while (bufferedInputStream.available() > 0) {

                    byte[] data=new byte[1024];
                    int x=bufferedInputStream.read(data);

//                    if(x==5 || x==6) { //5 adalah enq(enquiry) karakter yaitu katakter kontrol transmisi untuk mengecek apakah node yg berlawanan aktif
//                        break;
//                    }


                    String usartMsg = new String(data);

//                    usartMsg=usartMsg.substring(0,i);
                    usartMsg=usartMsg.replace("\0",""); //buang yang null dibelakang
                    usartMsg=usartMsg.replace("\n","");
//                    System.out.println(usartMsg);
                    if(usartMsg.equals("null")){

                        break;
                    }
                    System.out.println("FROM USART "+usartMsg);
                    String[] msg=usartMsg.split(",",2);
                    String[] source=msg[0].split(":",3);


                    if(source[0].equals("source")){
                        String msgToAPI=msg[1];
                        boolean isSensing=false;
                        String[] splitMSG = msgToAPI.split(",", 4);

                        if(!splitMSG[0].equals("intervalRequest")){
                            this.setApiResponse(source[1]);
                            msgToAPI= FormatMSG.formatToAPIFormat(splitMSG); //kalau dia data sensing di format terlebih dahulu
                            isSensing=true;
                            myApi.sendToServer(source[1],msgToAPI,isSensing);
                        }else {
                            String idNode = splitMSG[1].split(":",2)[1];
                            idNode=idNode.replace("\"","");
                            myApi.sendToServer(source[1],idNode,isSensing);

                            //kode ini tidak dipakai karena terlalu banyak blocking, sehingga ada kemungkinan node lain tidak dapat masuk
                            //solusi nya: biarkan saja, kekurangannya yaitu node yang baru aktif akan menjalankan sensing 1-2 kali(default sensing interval 1s)
                            //keunggulanya tidak berdampak pada node lain (tidak blocking main thread)
//                            boolean existNode = false;
//                            while (!existNode){
//                                for (NodeQueue nodeQueue : this.queueNode) {
//                                    if (nodeQueue.getAddress() == Long.parseLong(source[1])) {
//                                        existNode = true;
//                                        while (nodeQueue.emptyQueue()) {
//                                        }
//                                    }
//                                }
//                            }
                            this.setApiResponse(source[1]);


                        }


                    }


                    else{
                        this.setApiResponse("0");
                    }

                }

            }
            catch(PureJavaIllegalStateException e){
                BaseStationControllerUSART bs=new BaseStationControllerUSART(this.args);
                bs.queueNode=this.queueNode;
            }
            catch (IOException e) {
                System.out.println(e.getMessage());
            }

        }
    }



    /**
     * untuk debug ant, agar debug ant muncul
     */
    private static DefaultLogger getConsoleLogger() {
        DefaultLogger consoleLogger = new DefaultLogger();
        consoleLogger.setErrorPrintStream(System.err);
        consoleLogger.setOutputPrintStream(System.out);
        consoleLogger.setMessageOutputLevel(Project.MSG_INFO);
        return consoleLogger;
    }


    /**
     * modifikasi dari method time_synchronize.
     * Modifikasi pada method ini adalah dengan diganti agar menerima target
     */
    private void executeAtPreon(String path,String target) {
        DefaultLogger consoleLogger = getConsoleLogger();
        File buildFile = new File(path);
        Project antProject = new Project();
        antProject.setUserProperty("ant.file", buildFile.getAbsolutePath());
        antProject.addBuildListener(consoleLogger);

        antProject.fireBuildStarted();
        antProject.init();
        ProjectHelper helper = ProjectHelper.getProjectHelper();
        antProject.addReference("ant.ProjectHelper", helper);
        helper.parse(antProject, buildFile);
        antProject.executeTarget(target);
        antProject.fireBuildFinished(null);

    }



    public static void main(String[] args) {
        new BaseStationControllerUSART(args);
    }


    public void setApiResponse(String nodeAddress) {
        try {
            while (writing){} // karena proses push data sensing ke server dilakukan secara async (multi thread) maka ada kemungkinan 2 thread menulis secara bersamaan
            writing=true;
            String responseBS="";
            Long nodeAddess=Long.parseLong(nodeAddress);
            boolean existNode=false;
            for (NodeQueue nodeQueue: this.queueNode){
                if(nodeQueue.getAddress()==nodeAddess){
                    existNode=true;
                    if(nodeQueue.emptyQueue()){
                        responseBS =(nodeAddress+":ok");
                    }else {
                        String queueMsg=nodeQueue.getQueue();
                        queueMsg=queueMsg.replace("{","");
                        queueMsg=queueMsg.replace("}","");
                        queueMsg=queueMsg.replace("\"","");
                        queueMsg=nodeAddress+":"+queueMsg;
                        responseBS=queueMsg;
                    }
                    break;
                }
            }

            if(!existNode){
                responseBS =(nodeAddress+":ok");
            }
            System.out.println("TO USART "+responseBS);

            this.dataConnection.write(writeToBytes(responseBS),0,128);
            writing=false;
        } catch (IOException e) {
            System.out.println("failed api response");
            throw new RuntimeException(e);
        }

    }

    private byte[] writeToBytes(String msg){
        byte[] result=new byte[128];
        for(int i=0;i<msg.length();i++){
            result[i]= (byte) msg.charAt(i);
        }
        return result;

    }



}
