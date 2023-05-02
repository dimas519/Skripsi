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

	/** Gibt den freien zur Verf�gung stehenden Speicher zur�ck. */

	public static void printFreeMemory() {
		System.out.println("Free Memory: " + Runtime.getRuntime().freeMemory() + "[byte]");
	}

	/**
	 * Aktueller Thread wartet eine bestimmte Zeit.
	 *
	 * @param millis
	 *            Dauer in Millisekunden, die der aktuelle Thread anhalten soll.
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
	 * Bestimmt aus einem Array von byte[] einen String. Dabei ist das Ende
	 * eines Strings durch 0x00 definiert.
	 *
	 * @param b
	 *            Zeichenfeld, aus dem ein String erzeugt werden soll
	 *
	 * @return String, der aus byte[] gewandelt wurde
	 */
	public static String toString(byte[] b) {
		StringBuilder sb = new StringBuilder();
		for (int i = 0; i < b.length; i++) {
			byte buf = b[i];
			if (buf == 0x00) {
				break;
			}
			sb.append((char) buf);
		}
		return sb.toString();
	}

	/**
	 * Bringt eine Leuchtdiode zum blinken.
	 *
	 * @param led
	 *            Kodierung der LED je nach verwendeter Plattform
	 * @param millis
	 *            wie lange soll die LED ein- bzw. ausgeschaltet sein
	 * @param continiuos
	 *            soll die LED nur einmal oder fortlaufend blinken
	 */

	public static void LedBlinker(final LED led, final long millis, final boolean continiuos) {
		Thread thread = new Thread() {
			@Override
			public void run() {
				boolean running = true;
				while (running) {
					try {
						led.on();
						Misc.sleep(millis);
						led.off();
						Misc.sleep(millis);
					} catch (Exception e) {
						e.printStackTrace();
					}
					running = continiuos;
				}
			}
		};
		thread.start();
	}

	/**
	 * Unterprgramm zum Runden von Zahlen auf 2 Nachkommastellen
	 *
	 * @param value
	 *            Zahlenwert mit Nachkommastellen
	 *
	 * @return Zahlenwert mit maximale 2 Nachkommastellen
	 */
	public static double round(double value) {
		return ((int) (value * 100)) / 100.0;
	}
}