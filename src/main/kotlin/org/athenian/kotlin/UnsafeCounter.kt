package org.athenian.kotlin

import java.util.concurrent.CountDownLatch
import java.util.concurrent.Executors

fun main() {

    val JOB_COUNT = 1000
    val latch = CountDownLatch(JOB_COUNT)
    val executor = Executors.newCachedThreadPool()
    var count = 0

    repeat(JOB_COUNT) { i ->
        executor.submit {
            count++
            latch.countDown()
        }
    }

    // Wait for jobs to complete
    latch.await()

    println("count = $count")

    // Shutdown the thread pool before exiting
    executor.shutdown()
}
