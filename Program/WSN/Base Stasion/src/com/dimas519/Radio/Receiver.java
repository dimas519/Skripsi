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

import com.virtenio.driver.device.at86rf231.AT86RF231;
import com.dimas519.Radio.Misc;
import com.dimas519.Radio.RadioInit;

import com.virtenio.radio.ieee_802_15_4.Frame;

/**
 * Einfaches Beispiel der Funk�bertragung mit Senden und Empfangen.
 */
public class Receiver {

	private int COMMON_CHANNEL = 24;
	private int COMMON_PANID = 0xCAFE;
	private int ADDR_SEND = 0xAFFE;
	private int ADDR_RESV = 0xBABE;


	/** Ein Programme, dass �ber das Startmenu aufgerufen werden kann */

	public void prog_receiver() throws Exception {
		System.out.println("Text_Receiver");

		final AT86RF231 radio = RadioInit.initRadio();
		radio.setChannel(COMMON_CHANNEL);
		radio.setPANId(COMMON_PANID);
		radio.setShortAddress(ADDR_RESV);
		Thread reader = new Thread() {
			@Override
			public void run() {
				while (true) {
					Frame f = null;
					try {
						f = new Frame();
						radio.setState(AT86RF231.STATE_RX_AACK_ON);
						radio.waitForFrame(f);
					} catch (Exception e) {
					}

					if (f != null) {
						byte[] dg = f.getPayload();
						String str = new String(dg, 0, dg.length);
						String hex_addr = Integer.toHexString((int) f.getSrcAddr());
						System.out.println("FROM(" + hex_addr + "): " + str);
					}
				}
			}
		};
		reader.start();

		while (true) {
			Misc.sleep(1000);
		}
	}

}
