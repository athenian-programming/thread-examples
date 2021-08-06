package org.athenian.java;

import java.util.concurrent.CountDownLatch;

public class SimpleThread {

    public static void main(String[] args)
            throws InterruptedException {

        final CountDownLatch latch = new CountDownLatch(3);

        class MyThread extends Thread {
            @Override
            public void run() {
                long secs = 10;
                System.out.printf("IC thread sleeping %d secs...%n", secs);
                Utils.sleepSecs(secs);
                latch.countDown();
                System.out.println("IC thread finished");
            }
        }

        // Create a new Thread with an inner class
        Thread t0 = new MyThread();
        t0.setDaemon(true);
        t0.start();

        // Create a new Thread with an anonymous inner class
        Thread t1 = new Thread() {
            @Override
            public void run() {
                long secs = 8;
                System.out.printf("AIC thread sleeping %d secs...%n", secs);
                Utils.sleepSecs(secs);
                latch.countDown();
                System.out.println("AIC thread finished");
            }
        };
        t1.setDaemon(true);
        t1.start();

        // Create a new Thread with a lambda
        Thread t2 = new Thread(() -> {
            long secs = 5;
            System.out.printf("Lambda thread sleeping %d secs...%n", secs);
            Utils.sleepSecs(secs);
            latch.countDown();
            System.out.println("Lambda thread finished");
        });
        t2.setDaemon(true);
        t2.start();

        // Wait for both threads to complete
        System.out.println("Waiting for jobs to finish");
        latch.await();
        System.out.println("Done");
    }
}