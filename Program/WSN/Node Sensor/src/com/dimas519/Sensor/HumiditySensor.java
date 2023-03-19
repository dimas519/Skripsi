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

import com.virtenio.driver.device.SHT21;
import com.virtenio.driver.i2c.I2C;
import com.virtenio.driver.i2c.NativeI2C;

/**
 * Test den Zugriff auf den Sensor SHT21 von Sensirion �ber I2C.
 *
 * <p/>
 * <b> Datenblatt des Sensors: </b> <a href=
 * "http://www.sensirion.com/en/pdf/product_information/Datasheet-humidity-sensor-SHT21.pdf"
 * target="_blank">
 * http://www.sensirion.com/en/pdf/product_information/Datasheet
 * -humidity-sensor-SHT21.pdf</a> (Stand: 29.03.2011)
 */
public class HumiditySensor{
	private SHT21 sht21;

	public HumiditySensor(NativeI2C i2c){
		try {
			init(i2c);
		} catch (Exception e) {
			System.err.println("Humidity failed initialize");
		}
	}

	private void init(NativeI2C i2c) throws Exception {


		System.out.println("SHT21(Init)");
		sht21 = new SHT21(i2c);
		sht21.open();
		sht21.setResolution(SHT21.RESOLUTION_RH12_T14);
		sht21.reset();


		System.out.println("Done(Init)");
	}

	public float run() {
		try {
			if(!sht21.isOpened())sht21.open();
			sht21.startRelativeHumidityConversion();
			Thread.sleep(100);
			int rawRH = sht21.getRelativeHumidityRaw();
			float rh = SHT21.convertRawRHToRHw(rawRH);
			sht21.close() ;
			return rh;
		} catch (Exception e) {
			System.err.println("Humidity failed sensing"+e.getMessage());
			return Float.MIN_VALUE;
		}
	}

}
