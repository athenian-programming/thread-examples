package org.athenian.kotlin

import java.util.concurrent.Executors
import kotlin.random.Random

fun main() {

    val executor = Executors.newCachedThreadPool()
    val monitor = Object()

    executor.submit {
        while (true) {
            println("Worker thread waiting...")
            try {
                synchronized(monitor) {
                    monitor.wait()
                }
            } catch (e: InterruptedException) {
                e.printStackTrace()
            }

            println("Worker thread done waiting on monitor")
        }
    }

    (0..3).forEach { i ->
        executor.submit {
            while (true) {
                val sleepTime = Random.nextInt(5).toLong()
                println("Notifier thread($i) sleeping $sleepTime secs...")
                sleepSecs(sleepTime)

                println("Notifier thread($i) calling notify()")
                synchronized(monitor) {
                    monitor.notify()
                }
            }
        }
    }
}
