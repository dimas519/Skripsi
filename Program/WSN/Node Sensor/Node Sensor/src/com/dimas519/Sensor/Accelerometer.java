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

import java.util.Arrays;

import com.virtenio.driver.device.ADXL345;
import com.virtenio.driver.gpio.GPIO;
import com.virtenio.driver.gpio.NativeGPIO;
import com.virtenio.driver.spi.NativeSPI;

/**
 * Example for the Triple Axis Accelerometer sensor ADXL345
 */
public class Accelerometer extends Sensor{
	private ADXL345 accelerationSensor;
	private String name="a"; //nama disingkat karena max frame 802.15.4 itu 127 char

	public Accelerometer(){
		try {
			System.out.println("GPIO(Init)");

			GPIO accelIrqPin1 = NativeGPIO.getInstance(37);
			GPIO accelIrqPin2 = NativeGPIO.getInstance(25);
			GPIO accelCs = NativeGPIO.getInstance(20);

			System.out.println("SPI(Init)");
			NativeSPI spi = NativeSPI.getInstance(0);
			spi.open(ADXL345.SPI_MODE, ADXL345.SPI_BIT_ORDER, ADXL345.SPI_MAX_SPEED);

			System.out.println("ADXL345(Init)");
			accelerationSensor = new ADXL345(spi, accelCs);
			accelerationSensor.open();
			accelerationSensor.setDataFormat(ADXL345.DATA_FORMAT_RANGE_2G);
			accelerationSensor.setDataRate(ADXL345.DATA_RATE_3200HZ);
			accelerationSensor.setPowerControl(ADXL345.POWER_CONTROL_MEASURE);

			System.out.println("Done(Init)");
		} catch (Exception e) {
			System.err.println(name+" failed");
		}
	}


	public String run() {
		try {
			short[] values = new short[3];
			accelerationSensor.getValuesRaw(values, 0); //membaca xyz sensor berdasarkan offset (parameter kedua)


			//perlu dibagi dengan typ (256), angka diperoleh dari dokumentasi sensor adxl345.
			//typ merupakan angka mayoritas, jika lokasi suatu sumbu yang mengarah ke inti dibagi dengan 256 maka hasilnya mendekati 1g
			double[] inG=new double[3];


			inG[0]= Math.round(( values[0]/256.0) * 100.0) / 100.0;

			inG[1]= Math.round(( values[1]/256.0) * 100.0) / 100.0;
			inG[2]=Math.round(( values[2]/256.0) * 100.0) / 100.0;

			String result="\""+name+"\":"+Arrays.toString(inG);


			return result;
		} catch (Exception e) {
			System.err.println(name+" failed");
			String result=name+":null";
			return result;
		}

	}


}
