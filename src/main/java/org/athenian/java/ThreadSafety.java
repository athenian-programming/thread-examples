package org.athenian.java;

import java.util.concurrent.CountDownLatch;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.concurrent.locks.Lock;
import java.util.concurrent.locks.ReentrantLock;

public class ThreadSafety {

    public static void main(String... args)
            throws InterruptedException {

        final int JOB_COUNT = 100;
        final int INC_COUNT = 1_000;

        final CountDownLatch latch = new CountDownLatch(JOB_COUNT);
        final NonThreadSafeCounter nonThreadSafeCounter = new NonThreadSafeCounter();
        final SynchronizedMethodCounter synchronizedMethodCounter = new SynchronizedMethodCounter();
        final SynchronizedBlockCounter synchronizedBlockCounter = new SynchronizedBlockCounter();
        final LockCounter lockCounter = new LockCounter();
        final AtomicCounter atomicCounter = new AtomicCounter();

        for (int i = 0; i < JOB_COUNT; i++) {
            new Thread(
                    () -> {
                        for (int j = 0; j < INC_COUNT; j++) {
                            nonThreadSafeCounter.increment();
                            synchronizedMethodCounter.increment();
                            synchronizedBlockCounter.increment();
                            lockCounter.increment();
                            atomicCounter.increment();
                        }
                        // Indicate job is complete
                        latch.countDown();
                    }).start();
        }

        // Wait for all jobs to complete
        latch.await();

        System.out.printf("Non-thread-safe counter value = %d%n", nonThreadSafeCounter.value());
        System.out.printf("Synchronized method counter value = %d%n", synchronizedMethodCounter.value());
        System.out.printf("Synchronized block counter value = %d%n", synchronizedBlockCounter.value());
        System.out.printf("Lock counter value = %d%n", lockCounter.value());
        System.out.printf("Atomic counter value = %d%n", atomicCounter.value());
    }

    static class NonThreadSafeCounter {
        int count = 0;

        void increment() {
            this.count++;
        }

        int value() {
            return this.count;
        }
    }

    static class SynchronizedMethodCounter {
        int count = 0;

        synchronized void increment() {
            this.count++;
        }

        int value() {
            return this.count;
        }
    }

    static class SynchronizedBlockCounter {
        private final static Object OBJECT = new Object();
        int count = 0;

        void increment() {
            synchronized (this /* OBJECT */) {
                this.count++;
            }
        }

        int value() {
            return this.count;
        }
    }

    static class LockCounter {
        final Lock lock = new ReentrantLock();
        int count = 0;

        void increment() {
            lock.lock();
            try {
                this.count++;
            } finally {
                lock.unlock();
            }
        }

        int value() {
            return this.count;
        }
    }

    static class AtomicCounter {
        final AtomicInteger count = new AtomicInteger(0);

        void increment() {
            this.count.incrementAndGet();
        }

        int value() {
            return this.count.get();
        }
    }
}