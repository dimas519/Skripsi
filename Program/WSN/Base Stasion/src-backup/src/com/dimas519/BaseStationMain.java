package com.dimas519;



import com.dimas519.Radio.MyRadio;
import com.dimas519.USART.MyUsart;
import com.virtenio.vm.Time;


public class BaseStationMain {

	public static void main(String[] args) throws Exception {
		new BaseStationMain().run();
	}



	private final MyUsart myUsart;
	private final MyRadio myRadio;

	private final int COMMON_CHANNEL =24;
	private final int COMMON_PANID =0xCAFE;
	private final int ADDR_RESV =0X0000;
	private int intervalResponse=200;



	public BaseStationMain(){

		this.myUsart=new MyUsart();
		this.myRadio=new MyRadio( ADDR_RESV, COMMON_PANID, COMMON_CHANNEL);

	}

	public void run() throws Exception  {
//		OutputStream outputStream=myUsart.getOutputStream();

		int identifier=0x0000;
		boolean running=true;


		while (true){
//			this.myUsart.run();
			this.myRadio.receive();


			Thread.sleep(intervalResponse);
		}
	}



}
