package com.dimas519;

import com.virtenio.vm.Time;

import com.virtenio.misc.PropertyHelper;

public class Prog {


	public static void main(String[] args) {
		Time time=new Time();
		long currTime=time.currentTimeMillis();
		System.out.println("Hello World"+currTime);
		System.out.flush();






	}
}
