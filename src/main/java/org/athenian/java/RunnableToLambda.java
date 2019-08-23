package org.athenian.java;

import org.athenian.kotlin.Utils;

import java.util.Random;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public class RunnableToLambda {

  public static void main(String[] args)
      throws InterruptedException {

    final ExecutorService executor = Executors.newCachedThreadPool();
    final Random random = new Random();
    final CountDownLatch latch = new CountDownLatch(2);

    // Submit a job using an explicit Runnable
    executor.submit(
        new Runnable() {
          @Override
          public void run() {
            long secs = random.nextInt(10);
            System.out.println(String.format("Non-lambda thread sleeping %d secs...", secs));
            org.athenian.kotlin.Utils.sleepSecs(secs);
            latch.countDown();
            System.out.println("Non-lambda thread finished");
          }
        });

    // Submit a job using a lambda
    executor.submit(
        () -> {
          long secs = random.nextInt(10);
          System.out.println(String.format("Lambda thread sleeping %d secs...", secs));
          Utils.INSTANCE.sleepSecs(secs);
          latch.countDown();
          System.out.println("Lambda thread finished");
        });

    // Wait for both jobs to complete
    latch.await();

    // Shutdown the thread pool before exiting
    System.out.println("Shutting down Executor");
    executor.shutdown();
  }
}
