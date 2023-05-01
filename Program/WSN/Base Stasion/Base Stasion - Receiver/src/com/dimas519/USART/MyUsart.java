package com.dimas519.USART;

import com.dimas519.MainInterface;
import com.virtenio.driver.usart.NativeUSART;
import com.virtenio.driver.usart.USART;
import com.virtenio.driver.usart.USARTException;
import com.virtenio.driver.usart.USARTParams;

import java.io.OutputStream;

public class MyUsart{
    private USART usart;
    private MainInterface mainInterface;

    public MyUsart(MainInterface mainInterface){
        try {
            this.usart=this.configUSART();
        } catch (Exception e) {
            throw new RuntimeException(e);
        }
        this.mainInterface=mainInterface;
    }

    public OutputStream getOutputStream() throws USARTException {
        return this.usart.getOutputStream();
    }



    public void run() throws USARTException {
        int option=this.usart.read();
            switch (option) {
                case -1:

                    break;
                case 0:

//                    this.mainInterface()
                    break;


            }
    }


    private USART configUSART() throws Exception{
        int instanceID = 0;
        USARTParams params = new USARTParams(115200, USART.DATA_BITS_8, USART.STOP_BITS_1, USART.PARITY_NONE);;
        NativeUSART usart = NativeUSART.getInstance(instanceID);
        try {
            usart.close();
            usart.open(params);
            return usart;
        }
        catch(Exception e) {
            return null;
        }
    }





}
