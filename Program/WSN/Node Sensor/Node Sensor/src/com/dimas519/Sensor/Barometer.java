/*
 * Copyright (c) 2011., Virtenio GmbH
 * All rights reserved.
 *
 * Commercial software license.
 * Only for test and evaluation purposes.
 * Use in commercial products prohibited.
 * No distribution without permission by Virtenio.
 * Ask Virtenio for other type of license at info@virtenio.de
 *
 * Kommerzielle Softwarelizenz.
 * Nur zum Test und Evaluierung zu verwenden.
 * Der Einsatz in kommerziellen Produkten ist verboten.
 * Ein Vertrieb oder eine Ver�ffentlichung in jeglicher Form ist nicht ohne Zustimmung von Virtenio erlaubt.
 * F�r andere Formen der Lizenz nehmen Sie bitte Kontakt mit info@virtenio.de auf.
 */

package com.dimas519.Sensor;

import com.dimas519.Radio.Misc;
import com.virtenio.driver.device.MPL115A2;
import com.virtenio.driver.gpio.GPIO;
import com.virtenio.driver.gpio.NativeGPIO;
import com.virtenio.driver.i2c.NativeI2C;

/**
 *
 * Kelas Baromter merupakan kelas yang bertugas untuk menginisalisasi barometer(alat ukur kelembapan) dan melakukan pembacaan tekanan udara dengan satuan kPa.
 *
 */
public class Barometer extends Sensor{
	private MPL115A2 pressureSensor;
	private String name="Pa"; //nama disingkat karena max frame 802.15.4 itu 127 char


	public Barometer(NativeI2C i2c){
		try {
			init(i2c);
		} catch (Exception e) {
			System.err.println("Barometer failed initialize");
		}
	}
	@Override
	 void init(NativeI2C i2c) throws Exception {

		System.out.println("GPIO(Init)");
		GPIO resetPin = NativeGPIO.getInstance(24);
		GPIO shutDownPin = NativeGPIO.getInstance(12);

		System.out.println("MPL115A2(Init)");
		pressureSensor = new MPL115A2(i2c, resetPin, shutDownPin);
		pressureSensor.open();
		pressureSensor.setReset(false);
		pressureSensor.setShutdown(false);

		System.out.println("Done(Init)");
	}


	@Override
	public String run()  {
		try {
			pressureSensor.startBothConversion();
			Thread.sleep(MPL115A2.BOTH_CONVERSION_TIME);
			int pressurePr = pressureSensor.getPressureRaw();
			int tempRaw = pressureSensor.getTemperatureRaw();
			float pressure = pressureSensor.compensate(pressurePr, tempRaw);

			String result="\""+name+"\":"+Misc.round(pressure);
			return result;
		} catch (Exception e) {
			System.err.println(name+" failed");
			String result=name+":null";
			return result;
		}

	}
}
