package com.dimas519;

//Sensor

import com.dimas519.Radio.sendreceive.SendReceiveExample;
import com.dimas519.Sensor.Accelerometer;
import com.dimas519.Sensor.Barometer;
import com.dimas519.Sensor.HumiditySensor;
import com.dimas519.Sensor.TemperatureSensor;



import com.virtenio.driver.i2c.I2C;
import com.virtenio.driver.i2c.NativeI2C;
import com.virtenio.io.Console;


public class Prog {


	public static void main(String[] args) throws Exception {
		long interval=300000;
		interval=500;


		System.out.println("sensor starting");
		System.out.flush();

		System.out.println("I2C(Init)");
		NativeI2C i2c= NativeI2C.getInstance(1);
		i2c.open(I2C.DATA_RATE_400);

		System.out.println("Sensors init");
		TemperatureSensor temp =new TemperatureSensor(i2c);
		HumiditySensor hum=new HumiditySensor(i2c);
		Barometer bar=new Barometer(i2c);
		Accelerometer acc=new Accelerometer();
		System.out.println("Sensor Initialize done");
		System.out.flush();

		while (true){

			System.out.println(temp.run());
			System.out.println(hum.run());
			System.out.println(bar.run());
			System.out.println(acc.run());

			System.out.println("=====================");
			System.out.println(" ");


			System.out.flush();

			SendReceiveExample sr=new SendReceiveExample();
			sr.prog_receiver();










			Thread.sleep(interval);
		}
	}
}
