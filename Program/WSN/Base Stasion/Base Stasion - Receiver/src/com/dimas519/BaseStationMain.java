package com.dimas519;

//Sensor

import com.dimas519.Radio.MyRadio;

import com.dimas519.USART.MyUsart;
import com.virtenio.driver.usart.NativeUSART;
import com.virtenio.driver.usart.USART;
import com.virtenio.driver.usart.USARTParams;
import com.virtenio.vm.Time;

import java.io.OutputStream;


public class BaseStationMain implements MainInterface {

	public static void main(String[] args) throws Exception {
		new BaseStationMain().run();
	}



//	private final MyUsart myUsart;
//	private final MyRadio myRadio;
	private int intervalResponse=200;



	public BaseStationMain(){

//		this.myUsart=new MyUsart(this);
//		this.receiver=new Receiver();

	}

	public void run() throws Exception  {
//		OutputStream outputStream=myUsart.getOutputStream();

		int identifier=0x0000;
		boolean running=true;


		while (true){
			System.out.println("time"+ Time.currentTimeMillis());
			System.out.flush();

//			this.myUsart.run();
//			receiver.prog_receiver();


			Thread.sleep(intervalResponse);
		}
	}







	@Override
	public void setTime(Time time) {

	}
}
