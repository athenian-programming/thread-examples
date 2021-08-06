package org.athenian.kotlin

import java.util.concurrent.CountDownLatch
import java.util.concurrent.Executors

fun main() {

    val latch = CountDownLatch(2)
    val executor = Executors.newCachedThreadPool()

    // Submit a job using an explicit Runnable
    executor.submit(
        object : Runnable {
            override fun run() {
                val secs = 10L
                println("Non-lambda thread {${Thread.currentThread()} sleeping $secs secs...")
                sleepSecs(secs)
                latch.countDown()
                println("Non-lambda thread {${Thread.currentThread()} finished")
            }
        }
    )

    // Submit a job using a lambda
    executor.submit {
        val secs = 5L
        println("Lambda thread {${Thread.currentThread()} sleeping $secs secs...")
        sleepSecs(secs)
        latch.countDown()
        println("Lambda thread {${Thread.currentThread()} finished")
    }

    // Wait for both jobs to complete
    println("Waiting for both jobs to finish")
    latch.await()

    // Shutdown the thread pool before exiting
    println("Shutting down Executor")
    executor.shutdown()
}
