import java.io.File;


import org.apache.tools.ant.DefaultLogger;
import org.apache.tools.ant.Project;
import org.apache.tools.ant.ProjectHelper;


/**
 * args pada kelas ini
 *  0 : path ke buildUser.xml
 *  1 : path ke build.xml
 *  2 : port number to preon  //sesuaikan dengan yang di context 1
 *  3 : API endpoint
 */

public class NodeSensor {
    public static void main(String[] args) {
        new NodeSensor();
    }

    public NodeSensor(){
        this.executeAtPreon("buildUser.xml","context.set.1");//ubah ke context 1, atau context yg berisikan ant build untuk preon
        this.executeAtPreon("build.xml","cmd.module.run"); //jalankan modulenya


    }

    private static DefaultLogger getConsoleLogger() {
        DefaultLogger consoleLogger = new DefaultLogger();
        consoleLogger.setErrorPrintStream(System.err);
        consoleLogger.setOutputPrintStream(System.out);
        consoleLogger.setMessageOutputLevel(Project.MSG_INFO);
        return consoleLogger;
    }


    private void executeAtPreon(String path,String target) {
        DefaultLogger consoleLogger = getConsoleLogger();
        File buildFile = new File(path);
        Project antProject = new Project();
        System.out.println(buildFile.getAbsolutePath());
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



}
