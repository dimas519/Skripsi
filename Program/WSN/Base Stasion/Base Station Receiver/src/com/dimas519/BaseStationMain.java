package com.dimas519;


import com.dimas519.Radio.MyRadio;
import com.dimas519.USART.MyUsart;
import com.virtenio.vm.Time;

public class BaseStationMain implements MainInterface {

	private final MyUsart myUsart; //objek usart, untuk berkomunikasi dengan laptop/ pc
	private final MyRadio myRadio; //objeck radio, untuk berkomunikasi dengan ns


	//konfigurasi radio
	private final int COMMON_CHANNEL =24;
	private final int COMMON_PANID =0xCAFE;
	private final int myAddress =0X0000;


	/**
	 * Method yang pertama akan dijalankan
	 * @param args
	 */
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
		this.myUsart.send("start");
		this.myUsart.run();


	}

	@Override
	public void processMsg(long address, String[] msg) {
//		if(msg[0]!=null && msg[1]!= null) {
			if (msg[0].equals("bs")) { // kalau prefix nya bs,  artinya request sesuatu ke base stasion
				this.setTime(address); //pada saat ini feature hanya setTime dan request interval saja
				this.myUsart.send("source:" + address + "," + msg[1]); //untuk minta interval				}
			} else if (msg[0].equals("server") ) { // kaalau prefix nya bs artinya request sesuatu ke base stasion
				this.myUsart.send("source:" + address + "," + msg[1]);
			}
			else {
				this.myRadio.send(address,msg[0]+":"+msg[1]);
			}
//		}
	}




	private void setTime(long address) {
		String msg="setTime:"+ Time.currentTimeMillis();
		this.myRadio.send(address,msg);//mengirimkan kembali perintah settime dan valuenya
	}


}
