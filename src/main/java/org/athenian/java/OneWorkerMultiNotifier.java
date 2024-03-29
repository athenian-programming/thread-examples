package org.athenian.java;

import java.util.Random;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public class OneWorkerMultiNotifier {

    public static void main(String[] args) {

      final ExecutorService executor = Executors.newCachedThreadPool();
      final Object monitor = new Object();
      final Random random = new Random();

      executor.submit(() -> {
        while (true) {
          System.out.println("Worker thread waiting...");
          try {
            synchronized (monitor) {
              monitor.wait();
            }
          } catch (InterruptedException e) {
            e.printStackTrace();
          }

          System.out.println("Worker thread done waiting on monitor");
        }
      });

      for (int j = 0; j < 3; j++) {
        int i = j;
        executor.submit(() -> {
          while (true) {
            long sleepTime = random.nextInt(5);
            System.out.printf("Notifier thread(%d) sleeping %d secs...%n", i, sleepTime);
            Utils.sleepSecs(sleepTime);

            System.out.printf("Notifier thread(%d) calling notify()%n", i);
            synchronized (monitor) {
              monitor.notify();
            }
          }
        });
      }
    }
}
