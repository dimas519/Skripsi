


public class FormatMsg {
    public static String formatToAPIFormat(String json){
        String[] arrOfStr = json.split(",", 2);

        String result="{\"time\":\""+Waktu.getTime();
        result+="\","+arrOfStr[0];
        result+=",\"result\":{"+arrOfStr[1]+"}}";


        return result;
    }


}
