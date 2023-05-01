package com.dimas519;

//Sensor

import com.dimas519.Radio.RadioSender;
import com.dimas519.Sensor.*;


import com.virtenio.driver.i2c.I2C;
import com.virtenio.driver.i2c.NativeI2C;


public class NodeSensor {


	public static void main(String[] args) throws Exception {
		final String identifier="AAAA"; //ini public identifier, wajib unique

		long interval=300000;
		interval=1000;


		System.out.println("sensor starting");
		System.out.flush();

		System.out.println("I2C(Init)");
		NativeI2C i2c= NativeI2C.getInstance(1);
		i2c.open(I2C.DATA_RATE_400);

		System.out.println("Sensors init");
		Sensor[] sensors=new Sensor[4];
		sensors[0] =new Thermometer(i2c);
		sensors[1]=new Hygrometer(i2c);
		sensors[2]=new Barometer(i2c);
		sensors[3]=new Accelerometer();
		System.out.println("Sensor initialized");

		System.out.println("Radio init");
		RadioSender sr=new RadioSender();
		System.out.println("Radio initialized");

		System.out.flush();

		String sensing;
		while (true){
			sensing="\"idBS\":\""+identifier+"\"";
			for (Sensor sensor :sensors){
				sensing+=",";
				sensing+=sensor.run();

			}
			System.out.println(sensing);
			sr.prog_sender(sensing);


			System.out.println("===================================");
			System.out.println(" ");


			System.out.flush();

			Thread.sleep(interval);
		}
	}
}
