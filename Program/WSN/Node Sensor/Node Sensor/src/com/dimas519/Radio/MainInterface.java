package com.dimas519.Radio;

/**
 * sebuah interface yang menghubungkan thread radio receive dengan kelas utama (NodeSensor)
 */
public interface MainInterface {

    /**
     *  penjelasan terdapat pada kelas utama (NodeSensor)
     */
    void processMsg(long address, String[] msg);
}
