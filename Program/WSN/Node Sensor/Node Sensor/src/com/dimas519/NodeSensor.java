package com.dimas519;

import com.dimas519.Radio.*;
import com.dimas519.Sensor.*;
import com.virtenio.driver.i2c.I2C;
import com.virtenio.driver.i2c.I2CException;
import com.virtenio.driver.i2c.NativeI2C;
import com.virtenio.vm.Time;



public class NodeSensor implements MainInterface {
	private final String identifier; //ini public identifier, wajib unique
	private final int COMMON_CHANNEL; //channel node ini
	private final int COMMON_PANID; //pan id node ini
	private final int myAddress; // alamat node ini
	private final int myBSAddress; // alamat bs node ini
	private long interval; //selang waktu sensing dilakukan
	private final Sensor[] sensors; //array objek sensor yang terdapat pada sensor init
	private final MyRadio myRadio; //variabel objek radio, radio ini digunakan untuk berkomunikasi dengan bs
	private boolean timeSync=false; //variabel yang digunakan agar sensor menunggu waktu dari bs terlebih dahulu
	private String token; //variabel yang digunakan sebagai authentikasi
	/**
	 *
	 * Sebuah method yang akan dijalankan pada saat pertama kali node sensor aktif
	 *
	 */
	public static void main(String[] args)  {
		NodeSensor node=new NodeSensor();
		node.run();
	}


	/**
	 *
	 * Sebuah method yang digunakan untuk inisialisasi variabel-variabel pada kelas ini yang sudah ditentukan
	 *
	 */
	public NodeSensor() {


		System.out.println("Variable initialization");
		this.identifier="AAAc"; //ini public identifier, wajib unique

		this.COMMON_CHANNEL =24;
		this.COMMON_PANID =0xCAFE;
		this.myAddress =0X0002;
		this.myBSAddress=0x0000;
//		this.interval=300000;
		this.interval=1000;
//		this.interval=200;
		this.sensors=new Sensor[4];
		this.token="0eO2khwvgj";

		System.out.println("Variable initialized");



		System.out.println("I2C(Init)");
		NativeI2C i2c= NativeI2C.getInstance(1);
		try {
			i2c.open(I2C.DATA_RATE_400);
		} catch (I2CException e) {
			System.out.println("failed i2c");
		}

		System.out.println("Sensors init");
		this.sensors[0] =new Thermometer(i2c);
		this.sensors[1]=new Hygrometer(i2c);
		this.sensors[2]=new Barometer(i2c);
		this.sensors[3]=new Accelerometer();
		System.out.println("Sensor initialized");

		System.out.println("Radio init");
		this.myRadio=new MyRadio(this ,myAddress,COMMON_PANID,COMMON_CHANNEL);
		System.out.println("Radio initialized");

		System.out.flush();
	}


	/**
	 *
	 * Sebuah method yang bertugas untuk melakukan sensing setiap selang waktu tertentu.
	 * setelah melakukan sensing methods ini juga bertugas untuk mengirimkan data sensing ke bs
	 *
	 */
	private void sensing(){
		String sensing;
		long start, end,processTime;
		while (true){
			start=Time.currentTimeMillis();
			sensing = "server:\"time\":" + Time.currentTimeMillis() + ",\"key\":\""+this.token+"\",\"id\":\"" + this.identifier + "\"";
			for (Sensor sensor : this.sensors) {
				sensing += ",";
				sensing += sensor.run();
			}
			System.out.println(sensing);
			System.out.flush();
			this.myRadio.sendMSG(this.myBSAddress, sensing);

			System.out.println("===================================");
			System.out.println(" ");

			System.out.flush();
			end=Time.currentTimeMillis();
			processTime=end-start;
			Misc.sleep(this.interval-processTime);
		}
	}


	/**
	 *
	 * Sebuah method yang bertugas untuk melakukan meminta nilai-nilai lainnya yang dibutuhkan seperti waktu, interval, dll dari bs
	 * selain hal tersebut  ini juga bertugas untuk memanggil sensing jika variabel sudah diinisialisasi
	 */
	private void run(){
		this.myRadio.receive();
		System.out.println("getting time to Base Station");
		initializeTime();
		while(!timeSync){}
		System.out.println("getting time to Base Station done");
		sensing();
	}


	/**
	 *
	 * Sebuah method digunakan untuk mengirimkan informasi kepada bs kalau node ini meminta interval dan waktu
	 *
	 */
	private void initializeTime(){
		this.myRadio.sendMSG(this.myBSAddress,"bs:intervalRequest,\"node\":\""+this.identifier+"\"");
	}


	/**
	 *
	 * Sebuah method yang digunakan untuk memproses informasi dari radio yang dikirimkan oleh base stasion
	 *
	 * @param address sebuah parameter siapa address pengirimnya. untuk setTime dan setInterval hanya boleh dilakukan oleh address bsnya
	 *
	 * @param msg sebuah parameter array dengan index 0 berupa commandnya dan index 1 berupa valuenya
	 *            misalkan ["setInterval","5000"] maka commandnya untuk mengganti interval dan nilai interval barunya 5000ms
	 *
	 */
	@Override
	public void processMsg(long address, String[] msg) {
		if(address==this.myBSAddress) { //memastikan pengirimannya berasal dari base stasion
			if (msg[0].equals("setTime")) {
				Time.setCurrentTimeMillis(Long.parseLong(msg[1]));
				this.timeSync = true;

			} else if (msg[0].equals("setInterval")) {
				int inputInterval=Integer.parseInt(msg[1]);
				if(inputInterval>=1000){
					this.interval = Integer.parseInt(msg[1]);
				}else{
					System.out.println("Interval not updated because lower than 1ms");
				}

			}
		}
	}
}
