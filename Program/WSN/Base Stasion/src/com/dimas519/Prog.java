package com.dimas519;

import com.dimas519.Sensor.TemperatureSensor;




public class Prog {


	public static void main(String[] args) throws Exception {



		while (true){
			System.out.println("sensor starting");
			System.out.flush();
			TemperatureSensor temp =new TemperatureSensor();
			temp.run();
//			HumiditySensor hum=new HumiditySensor();
//			Barometer bar=new Barometer();
//			Accelerometer acc=new Accelerometer();
//
//			System.out.println(temp.run());
//			System.out.flush();
//			System.out.println(hum.run());
//			System.out.flush();
//
//			System.out.println(bar.run());
//			System.out.flush();
//			System.out.println(acc.run());
			System.out.flush();







			Thread.sleep(1000);
			System.out.println("Hello World");
			System.out.flush();
		}








	}
}
