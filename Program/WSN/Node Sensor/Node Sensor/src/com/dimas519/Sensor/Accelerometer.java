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

import com.dimas519.Radio.Misc;
import com.virtenio.driver.device.ADXL345;
import com.virtenio.driver.gpio.GPIO;
import com.virtenio.driver.gpio.NativeGPIO;
import com.virtenio.driver.i2c.NativeI2C;
import com.virtenio.driver.spi.NativeSPI;


/**
 *
 * Kelas Akselerometer merupakan kelas yang bertugas untuk menginisalisasi akselerometer(alat ukur akselerasi) dan melakukan pembacaan akselerasi.
 *
 */

public class Accelerometer extends Sensor{
	private ADXL345 accelerationSensor;
	private String name="a"; //nama disingkat karena max frame 802.15.4 itu 127 char



	public Accelerometer(){
		try {
			init(null); //cukup diset
		} catch (Exception e) {
			System.err.println(name+" failed");
		}
	}

	@Override
	void init(NativeI2C i2c) throws Exception {
		System.out.println("GPIO(Init)");

		GPIO accelCs = NativeGPIO.getInstance(20);

		System.out.println("SPI(Init)");
		NativeSPI spi = NativeSPI.getInstance(0);
		spi.open(ADXL345.SPI_MODE, ADXL345.SPI_BIT_ORDER, ADXL345.SPI_MAX_SPEED); //disesuaikan dengan parameter yang dibutuhkan (mode,bit order dan max speed)

		System.out.println("ADXL345(Init)");
		accelerationSensor = new ADXL345(spi, accelCs); //init sensor accelerasi
		accelerationSensor.open();
		accelerationSensor.setDataFormat(ADXL345.DATA_FORMAT_RANGE_2G); //diset max pembacaan sensor 2g saja
 		accelerationSensor.setDataRate(ADXL345.DATA_RATE_50HZ);  //rate data 50hz, 50 data dalam 1 detik, pembacaan akan dilakukan dengan interval-min 1 detik sehingga dicari rate yang kecil agar battery lebih hemat daya
		accelerationSensor.setPowerControl(ADXL345.POWER_CONTROL_AUTO_SLEEP); //auto sleep agar battery lebih hemat;

		System.out.println("Done(Init)");
	}

	@Override
	public String run() {
		try {
			short[] values = new short[3]; //variabel yang akan menyimpan nilai xyz
			accelerationSensor.getValuesRaw(values, 0); //membaca xyz sensor berdasarkan offset (parameter kedua)


			//perlu dibagi dengan typ (256), angka diperoleh dari dokumentasi sensor adxl345.
			//typ merupakan angka mayoritas, jika lokasi suatu sumbu yang mengarah ke inti dibagi dengan 256 maka hasilnya mendekati 1g
			double[] inG=new double[3];
			inG[0]= Misc.round( values[0]); //set agar dia desimal dengan presisi 2
			inG[1]= Misc.round( values[1]);
			inG[2]= Misc.round( values[2]);


			String result="\""+name+"\":"+Arrays.toString(inG); //mengubah array menjadi array
			return result;
		} catch (Exception e) {
			System.err.println(name+" failed");
			String result=name+":null";
			return result;
		}

	}




}
