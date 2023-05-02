import API.*;
import org.apache.tools.ant.BuildException;
import org.apache.tools.ant.DefaultLogger;
import org.apache.tools.ant.Project;
import org.apache.tools.ant.ProjectHelper;

import java.io.*;

import java.util.Scanner;

import com.virtenio.commander.toolsets.preon32.Preon32Helper;
import com.virtenio.commander.io.DataConnection;

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
    BufferedInputStream bufferedInputStream;

    public BaseStationControllerUSART(String[] args){
        this.executeAtPreon(args[0],"context.set.1");//ubah ke context 1, atau context yg berisikan ant build untuk preon



        try{
            this.executeAtPreon(args[1],"cmd.time.synchronize"); //time sync karena preon punya rtc tapi tidak ada battery untuk rtc jalan
//            this.executeAtPreon(args[1],"cmd.module.run"); //jalankan modulenya sudah diganti dengan run module

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

        this.myApi=new API(args[2]);
        this.runBaseStasionPC();




    }

    private void runBaseStasionPC(){
        System.out.println("System ready to use");

        PrintWriter out;
        BufferedReader in;
        Scanner sc=new Scanner(System.in);


        while(!false){
            try {
                byte[] data=new byte[1024];

                while(bufferedInputStream.available() > 0) {

                    bufferedInputStream.read(data);
                    int i=0;
                    while (i<1024){
                        if(data[i]==0){
                            break;
                        }
                        i++;
                    }

                    String usartMsg = new String(data);
                    usartMsg=usartMsg.substring(0,i);
                    usartMsg=usartMsg.replace("\n","");

                    if( !usartMsg.equals("Base Radio Station ready")   ) {
                        String result= FormatMSG.formatToAPIFormat(usartMsg);
                        System.out.println(result);
                        this.myApi.sendToServer(result);
                    }
                }

            } catch (IOException e) {
                throw new RuntimeException(e);
            }

//            try {
//
//
//
//                in = new BufferedReader(new InputStreamReader(clientSocket.getInputStream())); //ngebuang prompt terima, atau nanti bisa dimanfaatin buat check dia keterima gkString greeting = in.readLine();
//
//                String zigbeeReceive = in.readLine(); //bisa digunakan untuk cek apakah benar terkirim
//
//                if(zigbeeReceive!= null){
//                    System.out.println(zigbeeReceive);
//                    if( !zigbeeReceive.equals("connection made")) {
//                        String result=FormatMsg.formatToAPIFormat(zigbeeReceive);
//                        this.myApi.sendToServer(result);
//                    }
//                }
//
//
//
//
//
//
////                greeting = in.readLine();
////                System.out.println(greeting);
//
//            } catch (IOException e) {
//                System.out.println("error");
//            }


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

}
