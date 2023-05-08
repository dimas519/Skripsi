package com.dimas519.USART;


import com.dimas519.MainInterface;
import com.virtenio.driver.usart.NativeUSART;
import com.virtenio.driver.usart.USART;
import com.virtenio.driver.usart.USARTException;
import com.virtenio.driver.usart.USARTParams;


public class MyUsart {
    private USART usart;

    private final MainInterface mainInterface;
    private volatile boolean isWriting = false;

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
        USARTParams params = new USARTParams(115200, USART.DATA_BITS_8, USART.STOP_BITS_1, USART.PARITY_NONE);

        NativeUSART usart = NativeUSART.getInstance(instanceID);

        try {
            usart.close();
            usart.open(params);
            return usart;
        } catch (Exception e) {
            return null;
        }
    }

    public void run()  {
        while (true) {
            try {
                while (usart.available() > 0) {
                    byte[] input = new byte[64];
                    try {
                        usart.readFully(input,0,64);
                    } catch (USARTException e) {
                        System.out.println("usart read error" + e.getMessage());
                    }

                    String inputStr = new String(input);
                    inputStr=inputStr.replace("\0","");
                    inputStr=inputStr.replace("\n","");

                    //expected <address node:isi pesan)
                    String[] processStr = splitMSG(inputStr, ':');

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
                                this.mainInterface.processMsg(Long.parseLong(processStr[0]), isiPesan);
                            }catch (Exception e){}
                    }

                    isWriting = false;

                }
            } catch (USARTException e) {
                System.out.println(e.getMessage());
            }
        }


    }

    public void send(String msg) {
        try {
            while (isWriting) {
            }//tidak langsung writing karena satu siklus writing ditandai dengan response ok dari pc. dan pc tidak pernah mengkontak duluan
            isWriting = true;
            this.usart.write(msg.getBytes(), 0, msg.length());
            this.usart.flush();

        } catch (USARTException e) {
            System.out.println(e.getMessage());
        }
    }

    private String[] splitMSG(String inputStr, char regex) {
        String[] result = new String[]{null,null};



        for (int i = 0; i < inputStr.length(); i++) {
            if (inputStr.charAt(i) == regex) {
                String command = inputStr.substring(0, i);
                result[0] = command;
                command=inputStr.substring(i+1);
                result[1]=command;
                break;
            }
        }
        return result;

    }


}
