package org.athenian.java;

import java.util.Random;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.stream.IntStream;

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
        }
        catch (InterruptedException e) {
          e.printStackTrace();
        }

        System.out.println("Worker thread done waiting on monitor");
      }
    });

    IntStream.range(0, 3)
             .forEach((i) -> {
               executor.submit(() -> {
                 while (true) {
                   long sleepTime = random.nextInt(5);
                   System.out.println(String.format("Notifier thread(%d) sleeping %d secs...", i, sleepTime));
                   Utils.INSTANCE.sleepSecs(sleepTime);

                   System.out.println(String.format("Notifier thread(%d) calling notify()", i));
                   synchronized (monitor) {
                     monitor.notify();
                   }
                 }
               });
             });
  }
}
