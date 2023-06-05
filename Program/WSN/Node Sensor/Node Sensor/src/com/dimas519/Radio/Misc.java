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

package com.dimas519.Radio;

import com.virtenio.driver.led.LED;

/**
 * Zus�tzliche Hilfsfunktionen zu Programmen f�r den Sensorknoten und die
 * Integration ins Menu.
 */

public class Misc {

	/**
	 * Aktueller Thread wartet eine bestimmte Zeit.
	 * sebuah method yang bertugas untuk melakukan sleep pada suatu thread.
	 *
	 * @param millis
	 *            Dauer in Millisekunden, die der aktuelle Thread anhalten soll.
	 *            waktu dalam milidetik sebuah tread akan sleep
	 *
	 */
	public static void sleep(long millis) {
		if (millis > 0) {
			try {
				Thread.sleep(millis);
			} catch (InterruptedException e) {
			}
		}
	}

	/**
	 *
	 * Sebuah method yang berfungsi untuk memastikan desimal dengan presisi 2
	 *
	 * @param value nilai yang akan diubah presisinya
	 * @return nilai yang sudah dengan 2 presisi
	 */

	public static double round(double value) {
		return Math.round( value * 100.0) / 100.0;
	}

}