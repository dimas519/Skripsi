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

import com.virtenio.driver.device.ADT7410;
import com.virtenio.driver.i2c.I2C;
import com.virtenio.driver.i2c.NativeI2C;

/**
 * Test den Zugriff auf den Temperatursensor ADT7410 von Analog �ber I2C.
 * <p/>
 * <b> Datenblatt des Temperatursensors: </b> <a href=
 * "http://www.analog.com/static/imported-files/data_sheets/ADT7410.pdf"
 * target="_blank">
 * http://www.analog.com/static/imported-files/data_sheets/ADT7410.pdf</a>
 * (Stand: 29.03.2011)
 */
public class TemperatureSensor{
	private ADT7410 temperatureSensor;

	private void init() throws Exception {
		System.out.println("I2C(Init)");
		NativeI2C i2c = NativeI2C.getInstance(1);
		i2c.open(I2C.DATA_RATE_400);

		System.out.println("ADT7410(Init)");
		temperatureSensor = new ADT7410(i2c, ADT7410.ADDR_0, null, null);
		temperatureSensor.open();
		temperatureSensor.setMode(ADT7410.CONFIG_MODE_CONTINUOUS);

		System.out.println("Done(Init)");
	}

	public void run() {
		try {
			init();
			float celsius = temperatureSensor.getTemperatureCelsius();
			System.out.println(celsius);
		} catch (Exception e) {
			System.out.println("temperature failed");
//			return Float.MIN_VALUE;
		}

	}


}