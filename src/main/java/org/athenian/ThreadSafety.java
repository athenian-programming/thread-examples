package org.athenian;

import java.util.concurrent.CountDownLatch;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.stream.IntStream;

public class ThreadSafety {

  public static void main(String... args)
      throws InterruptedException {

    final int JOB_COUNT = 100;
    final int INC_COUNT = 1000;

    final ExecutorService executor = Executors.newCachedThreadPool();
    final CountDownLatch latch = new CountDownLatch(JOB_COUNT);
    final NonThreadSafeCounter nonThreadSafeCounter = new NonThreadSafeCounter();
    final SynchronizedMethodCounter synchronizedMethodCounter = new SynchronizedMethodCounter();
    final SynchronizedBlockCounter synchronizedBlockCounter = new SynchronizedBlockCounter();
    final AtomicCounter atomicCounter = new AtomicCounter();

    IntStream.range(0, JOB_COUNT)
             .forEach((i) ->
                          executor.submit(
                              () -> {
                                IntStream.range(0, INC_COUNT)
                                         .forEach((j) -> {
                                           nonThreadSafeCounter.increment();
                                           synchronizedMethodCounter.increment();
                                           synchronizedBlockCounter.increment();
                                           atomicCounter.increment();
                                         });
                                // Indicate job is complete
                                latch.countDown();
                              })
                     );

    // Wait for all jobs to complete
    latch.await();

    System.out.println(String.format("Non-thread-safe counter value = %d", nonThreadSafeCounter.value()));
    System.out.println(String.format("Synchronized method counter value = %d", synchronizedMethodCounter.value()));
    System.out.println(String.format("Synchronized block counter value = %d", synchronizedBlockCounter.value()));
    System.out.println(String.format("Atomic counter value = %d", atomicCounter.value()));

    // Shutdown the thread pool before exiting
    System.out.println("Shutting down Executor");
    executor.shutdown();
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

    synchronized int value() {
      return this.count;
    }
  }

  static class SynchronizedBlockCounter {
    private final static Object OBJECT = new Object();
    int count = 0;

    void increment() {
      synchronized (OBJECT) {
        this.count++;
      }
    }

    int value() {
      synchronized (OBJECT) {
        return this.count;
      }
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
