package org.athenian.kotlin

fun sleepSecs(secs: Long) {
    try {
        Thread.sleep(secs * 1000)
    } catch (e: InterruptedException) {
        e.printStackTrace()
    }
}