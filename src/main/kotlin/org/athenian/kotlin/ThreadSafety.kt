package org.athenian.kotlin

import java.util.concurrent.CountDownLatch
import java.util.concurrent.Executors
import java.util.concurrent.atomic.AtomicInteger

fun main() {

    val JOB_COUNT = 100
    val INC_COUNT = 1_000

    val executor = Executors.newCachedThreadPool()
    val latch = CountDownLatch(JOB_COUNT)
    val nonThreadSafeCounter = NonThreadSafeCounter()
    val synchronizedMethodCounter = SynchronizedMethodCounter()
    val synchronizedBlockCounter = SynchronizedBlockCounter()
    val atomicCounter = AtomicCounter()

    repeat(JOB_COUNT) { i ->
        executor.submit {
            repeat(INC_COUNT) {
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

class NonThreadSafeCounter {
    var count = 0

    fun increment() {
        this.count++
    }

    fun value() = count
}

class SynchronizedMethodCounter {
    var count = 0

    @Synchronized
    fun increment() {
        this.count++
    }

    fun value() = count
}

class SynchronizedBlockCounter {
    var count = 0

    fun increment() {
        synchronized(this /* OBJECT */) {
            count++
        }
    }

    fun value(): Int {
        return count
    }

    companion object {
        private val OBJECT = Any()
    }
}

class AtomicCounter {
    val count = AtomicInteger(0)

    fun increment() {
        count.incrementAndGet()
    }

    fun value() = count.get()
}
