

import java.io.IOException;
import java.net.InetAddress;
import java.time.*;
import java.time.format.DateTimeFormatter;


public class Waktu {

    public static String getTime() {
        LocalDateTime datetime = LocalDateTime.now();
        DateTimeFormatter format = DateTimeFormatter.ofPattern("yyyy-MM-dd-HH-mm-ss");
        return datetime.format(format);
    }

}
