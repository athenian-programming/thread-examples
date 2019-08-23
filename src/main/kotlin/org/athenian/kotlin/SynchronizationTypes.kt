package org.athenian.kotlin

class SynchronizationTypes {
    internal val instanceVal = Any()

    /****** Instance methods  */

    // Synchronized block in instance methods
    internal fun instanceMethod() {
        // Some method actions
        synchronized(instanceVal) {
            // Synchronized method actions
        }
        // Other method actions
    }

    // Synchronized instance methods
    @Synchronized
    internal fun syncInstanceMethod() {
        // Synchronized method actions
    }

    // Equivalent to syncInstanceMethod()
    internal fun nonsyncInstanceMethod() {
        synchronized(this) {
            // Synchronized method actions
        }
    }

    companion object {

        internal val staticVal = Any()

        /*
        The synchronized keyword can be used in 4 circumstances:
        Synchronized block in instance methods
        Synchronized instance methods
        Synchronized block in static methods
        Synchronized static methods
        */

        /****** Static methods  */

        // Synchronized block in static methods
        internal fun staticMethod() {
            // Some method actions
            synchronized(staticVal) {
                // Synchronized method actions
            }
            // Other method actions
        }

        // Synchronized static methods
        @Synchronized
        internal fun syncStaticMethod() {
            // Method actions
        }

        // Equivalent to syncStaticMethod()
        internal fun nonsyncStaticMethod() {
            synchronized(SynchronizationTypes::class.java) {
                // Method actions
            }
        }
    }

}
