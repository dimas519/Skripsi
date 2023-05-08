package com.dimas519;


import com.dimas519.Radio.MyRadio;
import com.dimas519.USART.MyUsart;
import com.virtenio.vm.Time;

public class BaseStationMain implements MainInterface {

	private final MyUsart myUsart;
	private final MyRadio myRadio;

	private final int COMMON_CHANNEL =24;
	private final int COMMON_PANID =0xCAFE;
	private final int myAddress =0X0000;

	int p=1;

	public static void main(String[] args)  {

		try {
			new BaseStationMain().run();
		} catch (Exception e) {
			System.out.println(e.getMessage());
		}
	}


	public BaseStationMain(){
		this.myUsart=new MyUsart(this);
		this.myRadio=new MyRadio(this, myAddress, COMMON_PANID, COMMON_CHANNEL);

	}

	public void run() throws Exception  {
		this.myRadio.receive();

		this.myUsart.run();

	}

	@Override
	public void processMsg(long address, String[] msg) {
//		if(msg[0]!=null && msg[1]!= null) {
			if (msg[0].equals("timeRequest")) {
				this.setTime(address);
			} else if (msg[0].equals("data")) {
				this.myUsart.send("source:" + address + "," + msg[1]);
			} else  {
				this.myRadio.send(address,msg[0]+":"+msg[1]);
			}
//		}
	}




	private void setTime(long address) {
		String msg="setTime:"+ Time.currentTimeMillis();
		this.myRadio.send(address,msg);
	}


}
