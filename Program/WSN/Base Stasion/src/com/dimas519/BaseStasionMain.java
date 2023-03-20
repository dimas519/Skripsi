package com.dimas519;

//Sensor

import com.dimas519.Radio.Receiver;


public class BaseStasionMain {


	public static void main(String[] args) throws Exception {
		long interval=300000;
		interval=500;


		while (true){

			new Receiver().prog_receiver();








			Thread.sleep(interval);
		}
	}
}
