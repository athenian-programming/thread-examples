package org.athenian.java;

import java.util.Random;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.stream.IntStream;

public class MultiWorkerOneNotifierWakeAll {

  public static void main(String[] args) {

    final ExecutorService executor = Executors.newCachedThreadPool();
    final Object monitor = new Object();
    final Random random = new Random();

    executor.submit(() -> {
      while (true) {
        long secs = random.nextInt(10);
        System.out.println(String.format("Notifier thread sleeping %d secs...", secs));
        Utils.sleepSecs(secs);

        System.out.println("Notifier thread waking all worker threads()");
        synchronized (monitor) {
          monitor.notifyAll();
        }
      }
    });

    IntStream.range(0, 3)
             .forEach((i) -> {
               executor.submit(() -> {
                 while (true) {
                   System.out.println(String.format("Worker thread(%d) waiting...", i));
                   try {
                     synchronized (monitor) {
                       monitor.wait();
                     }
                   }
                   catch (InterruptedException e) {
                     e.printStackTrace();
                   }

                   System.out.println(String.format("Main thread(%d) done waiting on monitor", i));
                 }
               });
             });
  }
}
