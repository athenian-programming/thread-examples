package org.athenian.java;

public class Utils {
    public static void sleepSecs(final long secs) {
        try {
            Thread.sleep(secs * 1_000);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }
}
