package com.dimas519.USART;


import com.dimas519.MainInterface;
import com.virtenio.driver.usart.NativeUSART;
import com.virtenio.driver.usart.USART;
import com.virtenio.driver.usart.USARTException;
import com.virtenio.driver.usart.USARTParams;


/**
 * Einfaches Beispiel der Funk�bertragung mit Senden und Empfangen.
 *
 *  * Sebuah kelas objek usart yang berfungsi untuk berkomunikasi dengan pc, laptop, rasp pi melalui interface usb
 */
public class MyUsart {
    private USART usart;

    private final MainInterface mainInterface;
    private volatile boolean isWriting = false; //sebuah variabel yang digunakan untuk mengecek apakah ada thread lain yang sedang menulis

    public MyUsart(MainInterface mainInterface) {
        this.mainInterface = mainInterface;
        try {
            this.usart = this.configUSART();
        } catch (Exception e) {
            throw new RuntimeException(e);
        }

    }

    private USART configUSART() throws Exception {
        int instanceID = 0;
        USARTParams params = new USARTParams(115200, USART.DATA_BITS_8, USART.STOP_BITS_1, USART.PARITY_NONE); // menggunakan usart speed 115200bps

        NativeUSART usart = NativeUSART.getInstance(instanceID);

        try {
            usart.close();
            usart.open(params);
            return usart;
        } catch (Exception e) {
            return null;
        }
    }


    /**
     *
     * Sebuah method yang digunakan untuk menerima masukan dari pc menggunalkan usart
     *
     */
    public void run()  {
        while (true) {
            try {
                while (usart.available() > 0) {
                    byte[] input = new byte[128]; //dibuat 128 karena max dari radio hanya 127.
                    try {
                        usart.readFully(input,0,128);
                    } catch (USARTException e) {
                        System.out.println("usart read error" + e.getMessage());
                    }

                    String inputStr = new String(input); //jadikan sebuah string
                    inputStr=inputStr.replace("\0",""); //buang null
                    inputStr=inputStr.replace("\n",""); //buang new line

                    //expected <address node:isi pesan)
                    String[] processStr = splitMSG(inputStr, ':'); //memisahkan perintah dan value dengan pemisahnya berupa kataker ':'

                    if( processStr[1].equals("ok")){
                        //do nothing
                    }else if (processStr[0]==null) {
                        /* ada kondisi dimana usart melakukan kontrol terhadap perangkat lain(dalam hal ini pc)
                        dengan berukar enq---enquire---(0x05) dengan ack(0x06) untuk menentukan apakah lawan aktif

                        pengecekan ini dibutuhkan karena format pada umumnya yang digunakan program <command:isi_command>
                        sehingga jika pesan enq/ack di split akan menjadi [null,5] untuk enq atau [null,6] untuk ack
                         */

                    }else{
                        //expected <command ke bs:isi> misalkan setInterval:1000
                        String[] isiPesan = splitMSG(processStr[1], ':');
                            try {
                                this.mainInterface.processMsg(Long.parseLong(processStr[0]), isiPesan); //proses masukan dari pc
                            }catch (Exception e){}
                    }

                    isWriting = false; // setelah di proses set kembali variabel writing ke false sebagai penanda kalau sudah selesai

                }
            } catch (USARTException e) {
                System.out.println(e.getMessage());
            }
        }


    }


    /**
     *
     * Sebuah method yang digunakan untuk mengirimkan pesam ke pc menggunakan usart
     *
     */
    public void send(String msg) {
        try {
            while (isWriting) {
            }//tidak langsung writing karena satu siklus writing ditandai dengan response ok dari pc. dan pc tidak pernah mengkontak duluan
            //perlu menunggu agar tidak tejadi penulisan berbarengan dengan pc

            isWriting = true;//set sedang menulis

            this.usart.write(msg.getBytes(), 0, msg.length());
            this.usart.flush();

        } catch (USARTException e) {
            System.out.println(e.getMessage());
        }
    }

    private String[] splitMSG(String msg,char regex){
        for (int i=0;i<msg.length();i++){
            if(msg.charAt(i)==regex){
                return new String[]{
                        msg.substring(0,i),
                        msg.substring(i+1)
                };
            }
        }
        return null;
    }


}
