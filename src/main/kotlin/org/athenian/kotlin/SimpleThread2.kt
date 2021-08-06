package org.athenian.kotlin

import org.athenian.java.Utils
import java.util.concurrent.atomic.AtomicBoolean
import kotlin.concurrent.thread

fun main() {
    val lock = Any()
    val finished = AtomicBoolean(false)
    val jobList = mutableListOf<Runnable>()

    val t0 = thread(start = true) {
        while (!finished.get()) {
            if (jobList.isNotEmpty()) {
                val job: Runnable
                synchronized(lock) {
                    job = jobList.removeFirst()
                }
                job.run()
            } else {
                println("Waiting for jobs")
                Thread.sleep(1000)
            }
        }
    }

    val job = Runnable {
        val secs: Long = 2
        System.out.printf("Job {${Thread.currentThread()} sleeping %d secs...%n", secs)
        Utils.sleepSecs(secs)
        println("Job {${Thread.currentThread()} finished")
    }

    println("Submitting first jobs")
    repeat(2) {
        synchronized(lock) {
            jobList += job
        }
    }

    println("Waiting to submit more jobs")
    Utils.sleepSecs(5)

    println("Submitting second jobs")
    repeat(2) {
        synchronized(lock) {
            jobList += job
        }
    }

    // Wait for both threads to complete
    println("Waiting for thread to finish")
    t0.join()
    println("Finished")
}
