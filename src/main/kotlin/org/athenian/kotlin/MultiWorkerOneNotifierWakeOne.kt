package org.athenian.kotlin

import java.util.concurrent.Executors
import kotlin.random.Random

fun main() {

    val executor = Executors.newCachedThreadPool()
    val monitor = Object()

    executor.submit {
        while (true) {
            val secs = Random.nextInt(10).toLong()
            println(String.format("Notifier thread sleeping %d secs...", secs))
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
                println(String.format("Worker thread(%d) waiting...", i))
                try {
                    synchronized(monitor) {
                        monitor.wait()
                    }
                } catch (e: InterruptedException) {
                    e.printStackTrace()
                }

                println(String.format("Main thread(%d) done waiting on monitor", i))
            }
        }
    }
}
