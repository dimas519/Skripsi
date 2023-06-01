package com.dimas519;

import java.time.LocalDateTime;
import java.time.ZoneOffset;
import java.time.format.DateTimeFormatter;


public class FormatMSG {
    private static  String timeFormat(String time){
        long epoch=Long.parseLong(time.split(":",2)[1]);
        epoch/=1000; //konversi ke detik

        LocalDateTime date = LocalDateTime.ofEpochSecond(epoch,0, ZoneOffset.ofHours(7));

        //format apinya
        DateTimeFormatter format = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss");
        String java_date = date.format(format);
        return java_date;
    }

    public static  String formatToAPIFormat(String[] splitMSG) {
        String dateConverted = FormatMSG.timeFormat(splitMSG[0]);
        String result="{\"time\":\""+dateConverted+"\","+splitMSG[1]+",\"result\":{"+splitMSG[2]+"}}";
        return result;


    }
}
