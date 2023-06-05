package com.dimas519.Sensor;

import com.virtenio.driver.i2c.NativeI2C;

abstract public class Sensor {
    public abstract String run();
    abstract void init(NativeI2C i2c) throws Exception;
}
