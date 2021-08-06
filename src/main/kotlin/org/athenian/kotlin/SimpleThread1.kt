package org.athenian.kotlin

import org.athenian.java.Utils
import java.util.concurrent.CountDownLatch
import kotlin.concurrent.thread

fun main() {
    val latch = CountDownLatch(2)

    // Create a new Thread with a Runnable
    val t0 = Thread(
        Runnable {
            val secs: Long = 5
            System.out.printf("Thread {${Thread.currentThread()} sleeping %d secs...%n", secs)
            Utils.sleepSecs(secs)
            latch.countDown()
            println("Thread {${Thread.currentThread()} finished")
        })
    t0.start()

    // Create a new Thread
    thread(start = true) {
        val secs: Long = 2
        System.out.printf("Thread {${Thread.currentThread()} sleeping %d secs...%n", secs)
        Utils.sleepSecs(secs)
        latch.countDown()
        println("Thread {${Thread.currentThread()} finished")
    }

    // Wait for both threads to complete
    println("Waiting for both jobs to finish.")
    latch.await()
}
