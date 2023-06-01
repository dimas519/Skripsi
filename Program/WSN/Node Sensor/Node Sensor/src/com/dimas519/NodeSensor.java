package com.dimas519;

import com.dimas519.Radio.*;
import com.dimas519.Sensor.*;
import com.virtenio.driver.i2c.I2C;
import com.virtenio.driver.i2c.I2CException;
import com.virtenio.driver.i2c.NativeI2C;
import com.virtenio.vm.Time;



public class NodeSensor implements RadioInterface {
	private final String identifier; //ini public identifier, wajib unique
	private final int COMMON_CHANNEL;
	private final int COMMON_PANID;
	private final int myAddress;
	private final int myBSAddress;
	private long interval;
	private final Sensor[] sensors;
	private final MyRadio myRadio;
	private boolean timeSync=false;



	public static void main(String[] args)  {
		NodeSensor node=new NodeSensor();
		node.run();
	}

	public NodeSensor() {

		System.out.println("Variable initialization");
		this.identifier="AAAc"; //ini public identifier, wajib unique
		this.COMMON_CHANNEL =24;
		this.COMMON_PANID =0xCAFE;
		this.myAddress =0X0001;
		this.myBSAddress=0x0000;
//		this.interval=300000;
		this.interval=1000;
//		this.interval=200;
		this.sensors=new Sensor[4];

		System.out.println("Variable initialized");




		System.out.println("I2C(Init)");
		NativeI2C i2c= NativeI2C.getInstance(1);
		try {
			i2c.open(I2C.DATA_RATE_400);
		} catch (I2CException e) {
			System.out.println("failed i2c");
		}

		System.out.println("Sensors init");
		this.sensors[0] =new Thermometer(i2c);
		this.sensors[1]=new Hygrometer(i2c);
		this.sensors[2]=new Barometer(i2c);
		this.sensors[3]=new Accelerometer();
		System.out.println("Sensor initialized");

		System.out.println("Radio init");
		this.myRadio=new MyRadio(this ,myAddress,COMMON_PANID,COMMON_CHANNEL);
		System.out.println("Radio initialized");


		System.out.flush();



	}

		private void sensing(){
			String sensing;
			long start, end,processTime;
			while (true){
				start=Time.currentTimeMillis();
				sensing = "server:\"time\":" + Time.currentTimeMillis() + ",\"idBS\":\"" + this.identifier + "\"";
				for (Sensor sensor : this.sensors) {
					sensing += ",";
					sensing += sensor.run();
				}
				System.out.println(sensing);
				System.out.flush();
				this.myRadio.sendMSG(this.myBSAddress, sensing);

				System.out.println("===================================");
				System.out.println(" ");

				System.out.flush();
				end=Time.currentTimeMillis();
				processTime=end-start;
				Misc.sleep(this.interval-processTime);
			}
	}

	private void run(){
		this.myRadio.receive();
		System.out.println("getting time to Base Station");
		initializeTime();
		while(!timeSync){}
		System.out.println("getting time to Base Station done");
		sensing();
	}

	private void initializeTime(){
		this.myRadio.sendMSG(this.myBSAddress,"bs:intervalRequest,\"idBS\":\""+this.identifier+"\"");
	}


	@Override
	public void processMsg(long address, String[] msg) {
		if(msg[0].equals("setTime")){
			Time.setCurrentTimeMillis(Long.parseLong(msg[1]));
			this.timeSync=true;
		}
		else if (msg[0].equals("setInterval")){
			this.interval=Integer.parseInt(msg[1]);
		}
	}
}
