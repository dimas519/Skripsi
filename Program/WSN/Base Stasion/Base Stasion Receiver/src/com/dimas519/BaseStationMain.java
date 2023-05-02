package com.dimas519;


import com.dimas519.Radio.MyRadio;
import com.dimas519.Radio.RadioInterface;
import com.dimas519.USART.MyUsart;
import com.virtenio.vm.Time;

public class BaseStationMain implements RadioInterface {

	private final MyUsart myUsart;
	private final MyRadio myRadio;

	private final int COMMON_CHANNEL =24;
	private final int COMMON_PANID =0xCAFE;
	private final int myAddress =0X0000;
	private int intervalResponse=200;

	public static void main(String[] args)  {

		try {
			new BaseStationMain().run();
		} catch (Exception e) {
			System.out.println(e.getMessage());
		}
	}


	public BaseStationMain(){
		this.myUsart=new MyUsart();
		this.myRadio=new MyRadio(this, myAddress, COMMON_PANID, COMMON_CHANNEL);

	}

	public void run() throws Exception  {
//		OutputStream outputStream=myUsart.getOutputStream();

		boolean running=true;

		this.myRadio.receive();
		while (true){
			this.myUsart.run();


			Thread.sleep(intervalResponse);
		}
	}

	@Override
	public void processMsg(long address, String[] msg) {
		if(msg[0].equals("timeRequest")){
			this.setTime(address);
		}else if(msg[0].equals("data")){
			this.data(msg[1]);
		}
	}


	private void setTime(long address) {
		String msg="setTime:"+ Time.currentTimeMillis();
		this.myRadio.send(address,msg);
	}

	private void data(String msg) {
		this.myUsart.send(msg);
	}


}
