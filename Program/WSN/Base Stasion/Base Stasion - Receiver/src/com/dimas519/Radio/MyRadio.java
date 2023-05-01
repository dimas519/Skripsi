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

import com.virtenio.io.Console;
import com.virtenio.radio.ieee_802_15_4.Frame;


/**
 * Einfaches Beispiel der Funk�bertragung mit Senden und Empfangen.
 */
public class MyRadio {

	private Console console;
	private final int COMMON_CHANNEL ;
	private final int COMMON_PANID ;
	private final int ADDR_RESV ;

	public MyRadio( ){
		this.console=new Console();
		this.COMMON_CHANNEL=24;
		this.COMMON_PANID=0xCAFE;
		this.ADDR_RESV=0X0000;
	}


	private int ADDR_SEND = 0X0001;






	/** Ein Programme, dass �ber das Startmenu aufgerufen werden kann */

	public void prog_receiver() throws Exception {
		System.out.println("connection made");
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
//						System.out.println("debug: FROM(" + hex_addr + "): " + str);
//						System.out.flush();
						console.println(str);
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
