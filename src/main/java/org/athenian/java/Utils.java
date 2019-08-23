package org.athenian.java;

public class Utils {
  public static void sleepSecs(final long secs) {
    try {
      Thread.sleep(secs * 1000);
    }
    catch (InterruptedException e) {
      e.printStackTrace();
    }
  }
}
