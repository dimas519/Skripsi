


import java.io.*;
import java.util.Scanner;


//package untuk melakukan aksi preon32. (aksi = menjalankan, sinkronisasi waktu,dll)
import API.API;
import org.apache.tools.ant.BuildException;
import org.apache.tools.ant.DefaultLogger;
import org.apache.tools.ant.Project;
import org.apache.tools.ant.ProjectHelper;

//package untuk berkomunikasi dengan preon32
import java.net.ServerSocket;
import java.net.Socket;


/**
 * args pada kelas ini
 *  0 : path ke buildUser.xml
 *  1 : path ke build.xml
 *  2 : port number to preon  //sesuaikan dengan yang di context 1
 *  3 : API endpoint
 */

public class BaseStationController {
    private ServerSocket serverSocket;
    private Socket clientSocket;

    private API myApi;


    public BaseStationController(String[] args){
        this.executeAtPreon(args[0],"context.set.1");//ubah ke context 1, atau context yg berisikan ant build untuk preon

        try{
            this.serverSocket=new ServerSocket(Integer.parseInt(args[2]));
        }catch (IOException e) {
            System.err.print("port error with msg:"+e.getMessage());
        }




        try{ //try catch dipindahkan dari execute at preon karena ada kemungkinan gagal koneksi ke preon( tidak terhubung). sehingga module.run tidak jalan
            this.executeAtPreon(args[1],"cmd.time.synchronize"); //time sync karena preon punya rtc tapi tidak ada battery untuk rtc jalan
            this.executeAtPreon(args[1],"cmd.module.run"); //jalankan modulenya

            this.myApi=new API(args[3]);
            this.runBaseStasionPC();


            
        }catch(BuildException e){
            System.err.print("com to preon problem with msg:"+e.getMessage());
        }
    }

    private void runBaseStasionPC(){
        System.out.println("System ready to use");
        try {
            clientSocket = serverSocket.accept();
        } catch (IOException e) {
            System.out.println("failed accept");
        }
        PrintWriter out;
        BufferedReader in;
        Scanner sc=new Scanner(System.in);


        while(!false){
            try {
                out = new PrintWriter(this.clientSocket.getOutputStream(), true);


                in = new BufferedReader(new InputStreamReader(clientSocket.getInputStream())); //ngebuang prompt terima, atau nanti bisa dimanfaatin buat check dia keterima gkString greeting = in.readLine();

                String zigbeeReceive = in.readLine(); //bisa digunakan untuk cek apakah benar terkirim

//                if(zigbeeReceive!= null){
//                    System.out.println(zigbeeReceive);
//                    if( !zigbeeReceive.equals("connection made")) {
//                        String result=FormatMsg.formatToAPIFormat(zigbeeReceive);
//                        this.myApi.sendToServer(result);
//                    }
//                }






//                greeting = in.readLine();
//                System.out.println(greeting);

            } catch (IOException e) {
                System.out.println("error");
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
        new BaseStationController(args);
    }

}
