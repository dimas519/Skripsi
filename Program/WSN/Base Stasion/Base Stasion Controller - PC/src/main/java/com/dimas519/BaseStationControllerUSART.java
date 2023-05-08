package com.dimas519;


import com.dimas519.retrofit.API;
import org.apache.tools.ant.BuildException;
import org.apache.tools.ant.DefaultLogger;
import org.apache.tools.ant.Project;
import org.apache.tools.ant.ProjectHelper;

import java.io.*;

import com.virtenio.commander.toolsets.preon32.Preon32Helper;
import com.virtenio.commander.io.DataConnection;

/**
 * args pada kelas ini
 *  0 : path ke buildUser.xml
 *  1 : path ke build.xml
 *  2 : port number to preon  //sesuaikan dengan yang di context 1
 *  3 : API endpoint
 */

public class BaseStationControllerUSART implements BaseStasionControllerInterface {

    private API myApi;
    private  Preon32Helper nodeHelper;
    private DataConnection dataConnection;
    private BufferedInputStream bufferedInputStream;
    private volatile boolean writing=false;

    public BaseStationControllerUSART(String[] args){
        this.executeAtPreon("buildUser.xml","context.set.1");//ubah ke context 1, atau context yg berisikan ant build untuk preon



        try{
            this.executeAtPreon("build.xml","cmd.time.synchronize"); //time sync karena preon punya rtc tapi tidak ada battery untuk rtc jalan

        }catch(BuildException e){
            System.err.print("com to preon problem with msg:"+e.getMessage());
        }


        try {
            this.nodeHelper = new Preon32Helper("COM8",115200);
            this.dataConnection = this.nodeHelper.runModule("autostart");
            bufferedInputStream = new BufferedInputStream(this.dataConnection.getInputStream());

        } catch (Exception e) {
            System.out.println("failed open connection to preon32");
        }

        this.myApi=new API(args[0],this);
        this.runBaseStasionPC();




    }

    private void runBaseStasionPC(){
        System.out.println("System ready to use");



        while(!false){
            try {

                while (bufferedInputStream.available() > 0) {

                    byte[] data=new byte[1024];
                    int x=bufferedInputStream.read(data);

                    if(x==5 || x==6) { //5 adalah enq(enquiry) karakter yaitu katakter kontrol transmisi untuk mengecek apakah node yg berlawanan aktif
                        break;
                    }


                    String usartMsg = new String(data);

//                    usartMsg=usartMsg.substring(0,i);
                    usartMsg=usartMsg.replace("\0",""); //buang yang null dibelakang
                    usartMsg=usartMsg.replace("\n","");
                    System.out.println(usartMsg);
                    if(usartMsg.equals("null")){

                        break;
                    }

                    String[] msg=usartMsg.split(",",2);
                    String[] source=msg[0].split(":",2);


                    if(source[0].equals("source")){
                        String format= FormatMSG.formatToAPIFormat(msg[1]);
                        System.out.println(format);

                        myApi.sendToServer(source[1],format);
                    }

                }

            } catch (IOException e) {
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

    @Override
    public void setApiResponse(String source,String response) {
        try {
            while (writing){} // karena proses push data sensing ke server dilakukan secara async (multi thread) maka ada kemungkinan 2 thread menulis secara bersamaan
            writing=true;
            String responseBS;
            if(response.equals("{\"result\":false}")|| response.equals("{\"result\":true}")){
                responseBS =(source+":ok");
            }else{
                response=response.replace("{","");
                response=response.replace("}","");
                response=response.replace("\"","");
                response=source+":"+response;
                responseBS=response;
            }
            System.out.println(response);
            this.dataConnection.write(writeToBytes(responseBS),0,64);
            writing=false;
        } catch (IOException e) {
            System.out.println("failed api response");
            throw new RuntimeException(e);
        }

    }

    private byte[] writeToBytes(String msg){
        byte[] result=new byte[64];
        for(int i=0;i<msg.length();i++){
            result[i]= (byte) msg.charAt(i);
        }
        return result;

    }



}
