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
import com.virtenio.driver.device.ADT7410;
import com.virtenio.driver.i2c.NativeI2C;

/**
 *
 * Kelas Thermometer merupakan kelas yang bertugas untuk menginisalisasi thermometer(alat ukur suhu) dan melakukan pembacaan tekanan udara dengan satuan celcius.
 *
 */
public class Thermometer extends Sensor{
	private ADT7410 temperatureSensor;
	private String name="T"; //nama disingkat karena max frame 802.15.4 itu 127 char

	public Thermometer(NativeI2C i2c){
		try {
			init(i2c);
		} catch (Exception e) {
			System.err.println("temperature failed initialize"+e);
		}

	}


	@Override
	 void init(NativeI2C i2c) throws Exception {
		System.out.println("ADT7410(Init)");
		temperatureSensor = new ADT7410(i2c, ADT7410.ADDR_0, null, null);
		temperatureSensor.open();
		temperatureSensor.setMode(ADT7410.CONFIG_MODE_CONTINUOUS);

		System.out.println("Done(Init)");
	}

	@Override
	public String run() {
		try {
			float celsius = temperatureSensor.getTemperatureCelsius();

			String result="\""+name+"\":"+ Misc.round(celsius);
			return result;
		} catch (Exception e) {
			System.out.println(name+" failed"+e.getMessage());
			String result=name+":null";
			return result;
		}

	}


}