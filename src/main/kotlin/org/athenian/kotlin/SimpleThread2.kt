package org.athenian.kotlin

import java.util.concurrent.atomic.AtomicBoolean
import kotlin.concurrent.thread

fun main() {
    val lock = Any()
    val finished = AtomicBoolean(false)
    val jobList = mutableListOf<Runnable>()

    val t0 = thread(start = true, name = "Job-Thread") {
        while (!finished.get() || jobList.isNotEmpty()) {
            if (jobList.isNotEmpty()) {
                val job: Runnable
                synchronized(lock) {
                    job = jobList.removeFirst()
                }
                job.run()
            } else {
                println("Waiting for jobs in ${Thread.currentThread()}")
                Thread.sleep(1_000)
            }
        }
    }

    Thread.sleep(5000)

    val job = Runnable {
        val secs: Long = 2000
        System.out.printf("Job {${Thread.currentThread()} sleeping %d ms...%n", secs)
        Thread.sleep(secs)
        println("Job {${Thread.currentThread()} finished")
    }

    println("Submitting first jobs")
    repeat(2) {
        synchronized(lock) {
            jobList += job
        }
    }

    println("Waiting to submit more jobs")
    Thread.sleep(5000)

    println("Submitting second jobs")
    repeat(2) {
        synchronized(lock) {
            jobList += job
        }
    }

    finished.set(true)

    // Wait for both threads to complete
    println("Waiting for thread to finish")
    t0.join()
    println("Finished")
}
