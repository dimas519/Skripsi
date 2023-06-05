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
import com.virtenio.driver.device.SHT21;
import com.virtenio.driver.i2c.NativeI2C;

/**
 *
 * Kelas Baromter merupakan kelas yang bertugas untuk menginisalisasi barometer(alat ukur tekanan) dan melakukan pembacaan tekanan udara dengan satuan kPa.
 *
 */
public class Hygrometer extends Sensor{
	private SHT21 sht21;
	private String name="rh"; //nama disingkat karena max frame 802.15.4 itu 127 char

	public Hygrometer(NativeI2C i2c){
		try {
			init(i2c);
		} catch (Exception e) {
			System.err.println("Humidity failed initialize");
		}
	}

	@Override
	 void init(NativeI2C i2c) throws Exception {


		System.out.println("SHT21(Init)");
		sht21 = new SHT21(i2c);
		sht21.open();
		sht21.setResolution(SHT21.RESOLUTION_RH12_T14);
		sht21.reset();


		System.out.println("Done(Init)");
	}

	@Override
	public String run() {
		try {
			sht21.startRelativeHumidityConversion();
			Thread.sleep(100);
			int rawRH = sht21.getRelativeHumidityRaw();
			float rh = SHT21.convertRawRHToRHw(rawRH);

			String result="\""+name+"\":"+ Misc.round(rh);
			return result;
		} catch (Exception e) {
			System.err.println(name+" failed"+e.getMessage());
			String result=name+":null";
			return result;
		}
	}

}
