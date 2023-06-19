package com.dimas519;

/**
 * Interface yang bertujuan agar dapat memproses pesan dikelas BaseStationMain
 */
public interface MainInterface {
    /**
     *
     * Method yang bergfungsi untuk memisahkan-misahkan pesan dari atau ke usart dan radio
     *
     * @param address alamat node yang mengirimkan/ tujuan
     * @param msg //isi pesan
     */
    void processMsg(long address, String[] msg);

}
