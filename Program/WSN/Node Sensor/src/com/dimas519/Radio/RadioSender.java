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
import com.virtenio.radio.ieee_802_15_4.Frame;

/**
 * Einfaches Beispiel der Funk�bertragung mit Senden und Empfangen.
 */
public class RadioSender {

	private int COMMON_CHANNEL = 24;
	private int COMMON_PANID = 0xCAFE;
	private int ADDR_SEND = 0X0001;
	private int ADDR_RESV = 0x0000;




	public void prog_sender(String msg) throws Exception {

		AT86RF231 radio = RadioInit.initRadio();
		radio.setChannel(COMMON_CHANNEL);
		radio.setPANId(COMMON_PANID);
		radio.setShortAddress(ADDR_SEND);


		boolean isOK = false;
		while (!isOK) {
			try {
				String message = msg;
				// ///////////////////////////////////////////////////////////////////////
				Frame frame = new Frame(Frame.TYPE_DATA | Frame.ACK_REQUEST
						| Frame.DST_ADDR_16 | Frame.INTRA_PAN | Frame.SRC_ADDR_16);
				frame.setSrcAddr(ADDR_SEND);
				frame.setSrcPanId(COMMON_PANID);
				frame.setDestAddr(ADDR_RESV);
				frame.setDestPanId(COMMON_PANID);
				radio.setState(AT86RF231.STATE_TX_ARET_ON);
				frame.setPayload(message.getBytes());
				radio.transmitFrame(frame);
				// ///////////////////////////////////////////////////////////////////////
				isOK = true;
			} catch (Exception e) {

			}
		}

		// radio.close();
	}


}
