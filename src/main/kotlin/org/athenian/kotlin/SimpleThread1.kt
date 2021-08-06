package org.athenian.kotlin

import java.util.concurrent.CountDownLatch
import kotlin.concurrent.thread

fun main() {
    val latch = CountDownLatch(2)

    // Create a new Thread with a Runnable
    val t0 = Thread(
        Runnable {
            val secs: Long = 5000
            System.out.printf("Thread {${Thread.currentThread()} sleeping %d ms...%n", secs)
            Thread.sleep(secs)
            latch.countDown()
            println("Thread {${Thread.currentThread()} finished")
        })
    t0.start()

    // Create a new Thread
    thread(start = true, name = "MyThread") {
        val secs: Long = 2000
        System.out.printf("Thread {${Thread.currentThread()} sleeping %d ms...%n", secs)
        Thread.sleep(secs)
        latch.countDown()
        println("Thread {${Thread.currentThread()} finished")
    }

    // Wait for both threads to complete
    println("Waiting for both jobs to finish on ${Thread.currentThread()}")
    latch.await()
    println("Done")
}
