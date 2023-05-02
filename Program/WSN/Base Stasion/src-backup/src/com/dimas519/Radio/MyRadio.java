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

import com.virtenio.driver.device.at86rf231.AT86RF231RadioDriver;
import com.virtenio.io.Console;
import com.virtenio.radio.ieee_802_15_4.Frame;
import com.virtenio.radio.ieee_802_15_4.FrameIO;
import com.virtenio.radio.ieee_802_15_4.RadioDriver;
import com.virtenio.radio.ieee_802_15_4.RadioDriverFrameIO;


/**
 * Einfaches Beispiel der Funk�bertragung mit Senden und Empfangen.
 */
public class MyRadio {



	private final FrameIO frameIO;
	private final AT86RF231 radio;



	public MyRadio( int resv, int panID,int channel){

		//interface yang digunakan untuk berhubungan dengan kelas main

		//inisialisasi radio
		try {
			this.radio=RadioInit.initRadio();
			this.radio.setChannel(channel);
			this.radio.setPANId(panID);
			this.radio.setShortAddress(resv);
			RadioDriver driver = new AT86RF231RadioDriver(this.radio);
			this.frameIO=new RadioDriverFrameIO(driver);
			System.out.println("Base Radio Station ready");
		} catch (Exception e) {
			throw new RuntimeException(e);
		}



	}




	public void send(int sendAddress, String msg) throws Exception {
		boolean isOK = false;
		while (!isOK) {
			try {
				// ///////////////////////////////////////////////////////////////////////
				Frame frame = new Frame(Frame.TYPE_DATA | Frame.ACK_REQUEST
						| Frame.DST_ADDR_16 | Frame.INTRA_PAN | Frame.SRC_ADDR_16);
				frame.setSrcAddr(this.radio.getShortAddress());
				frame.setSrcPanId(this.radio.getPANId());
				frame.setDestAddr(sendAddress);
				frame.setDestPanId(this.radio.getPANId());// karena untuk berkomunikasi dia butuh dalam satu pan(personal network)
				frame.setPayload(msg.getBytes());
				this.frameIO.transmit(frame);


				isOK = true;
			} catch (Exception e) {

			}
		}
		 this.radio.close();
	}




	/** Ein Programme, dass �ber das Startmenu aufgerufen werden kann */

	public void receive() throws Exception {
		System.out.println("Listening");
		Thread receive = new Thread(() -> {
			while (true) {
				Frame f = null;
				try {
					f = new Frame();
					frameIO.receive(f);
				} catch (Exception e) {}

				if (f != null) {
					byte[] dg = f.getPayload();
					String str = new String(dg, 0, dg.length);
					String hex_addr = Integer.toHexString((int) f.getSrcAddr());
//
					System.out.println(str);
					System.out.flush();


				}
				System.out.println("running receive");
				System.out.flush();
			}
		});
		receive.start();
	}

}
