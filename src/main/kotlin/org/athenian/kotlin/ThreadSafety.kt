package org.athenian.kotlin

import java.util.concurrent.CountDownLatch
import java.util.concurrent.Executors
import java.util.concurrent.atomic.AtomicInteger

fun main() {

    val JOB_COUNT = 100
    val INC_COUNT = 1000

    val executor = Executors.newCachedThreadPool()
    val latch = CountDownLatch(JOB_COUNT)
    val nonThreadSafeCounter = NonThreadSafeCounter()
    val synchronizedMethodCounter = SynchronizedMethodCounter()
    val synchronizedBlockCounter = SynchronizedBlockCounter()
    val atomicCounter = AtomicCounter()

    (0..JOB_COUNT)
        .forEach { i ->
            executor.submit {
                (0..INC_COUNT)
                    .forEach { j ->
                        nonThreadSafeCounter.increment()
                        synchronizedMethodCounter.increment()
                        synchronizedBlockCounter.increment()
                        atomicCounter.increment()
                    }
                // Indicate job is complete
                latch.countDown()
            }
        }

    // Wait for all jobs to complete
    latch.await()

    println("Non-thread-safe counter value = ${nonThreadSafeCounter.value()}")
    println("Synchronized method counter value = ${synchronizedMethodCounter.value()}")
    println("Synchronized block counter value = ${synchronizedBlockCounter.value()}")
    println("Atomic counter value = ${atomicCounter.value()}")

    // Shutdown the thread pool before exiting
    println("Shutting down Executor")
    executor.shutdown()
}

internal class NonThreadSafeCounter {
    var count = 0

    fun increment() {
        this.count++
    }

    fun value() = count
}

internal class SynchronizedMethodCounter {
    var count = 0

    @Synchronized
    fun increment() {
        this.count++
    }

    @Synchronized
    fun value() = count
}

internal class SynchronizedBlockCounter {
    var count = 0

    fun increment() {
        synchronized(OBJECT) {
            count++
        }
    }

    fun value(): Int {
        synchronized(OBJECT) {
            return count
        }
    }

    companion object {
        private val OBJECT = Any()
    }
}

internal class AtomicCounter {
    val count = AtomicInteger(0)

    fun increment() {
        count.incrementAndGet()
    }

    fun value() = count.get()
}
