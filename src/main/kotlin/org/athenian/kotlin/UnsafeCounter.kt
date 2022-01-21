package org.athenian.kotlin

import java.util.concurrent.CountDownLatch
import kotlin.concurrent.thread

fun main() {

    val JOB_COUNT = 100
    val INC_COUNT = 1_000
    val latch = CountDownLatch(JOB_COUNT)
    var count = 0

    repeat(JOB_COUNT) { i ->
        thread {
            repeat(INC_COUNT) {
                count++
            }
            latch.countDown()
        }
    }

    // Wait for jobs to complete
    latch.await()

    println("count = $count")
}
