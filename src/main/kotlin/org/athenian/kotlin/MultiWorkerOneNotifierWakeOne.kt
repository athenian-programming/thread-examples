package org.athenian.kotlin

import java.util.concurrent.Executors
import kotlin.random.Random

fun main() {

    val executor = Executors.newCachedThreadPool()
    val monitor = Object()

    executor.submit {
        while (true) {
            val secs = Random.nextInt(10).toLong()
            println("Notifier thread sleeping $secs secs...")
            sleepSecs(secs)

            println("Notifier thread waking a single worker thread()")
            synchronized(monitor) {
                monitor.notify()
            }
        }
    }

    (0..3).forEach { i ->
        executor.submit {
            while (true) {
                println("Worker thread($i) waiting...")
                try {
                    synchronized(monitor) {
                        monitor.wait()
                    }
                } catch (e: InterruptedException) {
                    e.printStackTrace()
                }

                println("Main thread($i) done waiting on monitor")
            }
        }
    }
}
