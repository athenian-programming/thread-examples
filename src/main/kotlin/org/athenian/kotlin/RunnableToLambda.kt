package org.athenian.kotlin

import java.util.concurrent.CountDownLatch
import java.util.concurrent.Executors
import kotlin.random.Random

fun main() {

    val executor = Executors.newCachedThreadPool()
    val latch = CountDownLatch(2)

    // Submit a job using an explicit Runnable
    executor.submit {
        val secs = Random.nextInt(10).toLong()
        println("Non-lambda thread sleeping $secs secs...")
        sleepSecs(secs)
        latch.countDown()
        println("Non-lambda thread finished")
    }

    // Submit a job using a lambda
    executor.submit {
        val secs = Random.nextInt(10).toLong()
        println("Lambda thread sleeping $secs secs...")
        sleepSecs(secs)
        latch.countDown()
        println("Lambda thread finished")
    }

    // Wait for both jobs to complete
    latch.await()

    // Shutdown the thread pool before exiting
    println("Shutting down Executor")
    executor.shutdown()
}
