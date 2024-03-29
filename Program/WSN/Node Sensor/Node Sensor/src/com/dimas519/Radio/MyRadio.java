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
import com.virtenio.radio.ieee_802_15_4.Frame;
import com.virtenio.radio.ieee_802_15_4.FrameIO;
import com.virtenio.radio.ieee_802_15_4.RadioDriver;
import com.virtenio.radio.ieee_802_15_4.RadioDriverFrameIO;


/**
 * Einfaches Beispiel der Funk�bertragung mit Senden und Empfangen.
 *
 * Sebuah kelas objek radio yang berfungsi untuk menerima dan mengirimkan pesan ke bs
 */
public class MyRadio {



	private  FrameIO frameIO;
	private  AT86RF231 radio;
	private final MainInterface mainInterface;


	/**
	 *
	 * method ini bertujuan untuk mengisisialisasi radio agar siap digunakan dalam bertukar pesan dengan bs
	 *
	 * @param mainInterface sebuah interface yang digunakan untuk berinteraksi dengan kelas utama node sensor(NodeSensor)
	 *
	 * @param resv alamat node ini
	 *
	 * @param panID personal area networks node ini
	 *
	 * @param channel channel node ini
	 *
	 */
	public MyRadio(MainInterface mainInterface, int resv, int panID, int channel){

		this.mainInterface=mainInterface;

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
			System.out.println("failed radio");
		}



	}


	/**
	 *
	 * Sebuah method yang berfungsi untuk mengirimkan pesan ke tujuan
	 *
	 * @param sendAddress alamat tujuan pesan
	 *
	 * @param msg isi pesannya
	 *
	 */
	public void sendMSG(int sendAddress, String msg)  {
		Exception tempEx;
		for (int i = 0; i < 9; i++) {
				try {
					// ///////////////////////////////////////////////////////////////////////
					Frame frame = new Frame(Frame.TYPE_DATA | Frame.ACK_REQUEST
							| Frame.DST_ADDR_16 | Frame.INTRA_PAN | Frame.SRC_ADDR_16);
					frame.setSrcAddr(this.radio.getShortAddress());
					frame.setSrcPanId(this.radio.getPANId());
					frame.setDestAddr(sendAddress);
					frame.setDestPanId(this.radio.getPANId());// karena untuk berkomunikasi dia butuh dalam satu pan(personal network)
					frame.setPayload(msg.getBytes());
					this.frameIO.transmit(frame); //kirimkan framenya
					break;
				} catch (Exception e) {
					tempEx=e;
				}

				if(i==8){ //kalau sampai 8 kali gagal kemungkinan alamat tujuannya tidak aktif, diluar jangkauan atau salah.
					System.out.println("**************************************************************");
					System.out.println(" failed send msg to " + sendAddress );
					tempEx.printStackTrace();
					System.out.println("**************************************************************");
				}

			}

	}


	/**
	 * Ein Programme, dass �ber das Startmenu aufgerufen werden kann
	 *
	 * sebuah method yang bertugas untuk menemerima pesan yang ditujukan untuk node ini di thread miliknya sendiri.
	 * kemudian akan memproses pesan tersebut/
	 *
	 *
	 * */
	public void receive() {
		Thread receive = new Thread()  {
			@Override
			public void run() {
				while (true) {
					Frame f = null;
					try {
						f = new Frame();
						frameIO.receive(f);
					} catch (Exception e) {
					}

					if (f != null) {
						byte[] dg = f.getPayload();
						String msg = new String(dg, 0, dg.length);
						long sourceAddress =  f.getSrcAddr(); //pengirimnya

						System.out.println("Radio receive: "+msg);
						String[] splittedMSG=splitMSG(msg,':'); //memisahkan perintah dan nilainya
						mainInterface.processMsg(sourceAddress,splittedMSG); //memproses perintah

					}
				}
			}
		};
		receive.start();
	}


	/**
	 *
	 * sebuah method yang berfungsi untuk memisahkan perintah dan nilainya
	 *
	 * @param msg pesan yang belum dipisahkan
	 *
	 * @param regex karakter pemisah pesan dan nilai
	 *
	 * @return array string berukuran 2 dengan index 0 berupa perintah dan index 1 berupa nilainya
	 */
	private String[] splitMSG(String msg,char regex){
		for (int i=0;i<msg.length();i++){
			if(msg.charAt(i)==regex){
				return new String[]{
						msg.substring(0,i),
						msg.substring(i+1)
				};
			}
		}
		return null;

	}
	
}
