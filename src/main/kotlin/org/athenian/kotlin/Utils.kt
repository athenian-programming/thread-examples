package org.athenian.kotlin

fun sleepSecs(secs: Long) {
    try {
        Thread.sleep(secs * 1_000)
    } catch (e: InterruptedException) {
        e.printStackTrace()
    }
}