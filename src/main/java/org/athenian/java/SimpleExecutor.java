package org.athenian.java;

import java.util.concurrent.CountDownLatch;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public class SimpleExecutor {

    public static void main(String[] args)
            throws InterruptedException {

        final CountDownLatch latch = new CountDownLatch(2);
        final ExecutorService executor = Executors.newCachedThreadPool();

        // Submit a job using an explicit Runnable
        executor.submit(
                new Runnable() {
                    @Override
                    public void run() {
                        long secs = 8;
                        System.out.printf("Non-lambda thread sleeping %d secs...%n", secs);
                        Utils.sleepSecs(secs);
                        latch.countDown();
                        System.out.println("Non-lambda thread finished");
                    }
                });

        // Submit a job using a lambda
        executor.submit(
                () -> {
                    long secs = 5;
                    System.out.printf("Lambda thread sleeping %d secs...%n", secs);
                    Utils.sleepSecs(secs);
                    latch.countDown();
                    System.out.println("Lambda thread finished");
                });

        // Wait for both jobs to complete
        System.out.println("Waiting for jobs to finish");
        latch.await();

        // Shutdown the thread pool before exiting
        System.out.println("Shutting down Executor");
        executor.shutdown();
    }
}