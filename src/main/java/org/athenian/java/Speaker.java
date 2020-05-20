package org.athenian.java;

import java.util.concurrent.CountDownLatch;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public class Speaker implements Runnable {

    private final String msg;
    private final long delay;
    private final CountDownLatch latch;

    public Speaker(String msg, long delay, CountDownLatch latch) {
        this.msg = msg;
        this.delay = delay;
        this.latch = latch;
    }

    public static void main(String[] args) throws InterruptedException {

        ExecutorService executor = Executors.newCachedThreadPool();

        int cnt = 10;

        CountDownLatch latch = new CountDownLatch(cnt);

        System.out.println("Firing off threads");

        for (int i = 0; i < cnt; i++) {
            Speaker actor = new Speaker("I am here #" + i, 500, latch);
            executor.submit(actor);
        }

        System.out.println("Waiting to finish");
        latch.await();
        System.out.println("Finished");

        executor.shutdown();
        System.exit(0);
    }

    @Override
    public void run() {
        for (int i = 0; i < 10; i++) {
            System.out.println(msg);

            try {
                Thread.sleep(delay);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }

        latch.countDown();
    }
}