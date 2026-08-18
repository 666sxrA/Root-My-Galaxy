package dev.busung.s25uroot

import android.app.Application
import java.io.File
import java.security.MessageDigest
import java.util.UUID

class F956bTestApplication : Application() {
    override fun onCreate() {
        super.onCreate()
        runCatching { importF956bTestLog() }
    }

    private fun importF956bTestLog() {
        val logFile = File(filesDir, TEST_LOG_FILE)
        if (!logFile.isFile || logFile.length() == 0L) return

        val bytes = logFile.readBytes()
        val digest = MessageDigest.getInstance("SHA-256")
            .digest(bytes)
            .joinToString("") { "%02x".format(it) }
        val preferences = getSharedPreferences(IMPORT_STATE, MODE_PRIVATE)
        if (preferences.getString(LAST_IMPORTED_SHA256, null) == digest) return

        val raw = bytes.toString(Charsets.UTF_8).replace("\r", "")
        val succeeded = raw.contains("exploit completed") && raw.contains("done=1 root=1")
        val now = System.currentTimeMillis()
        val entry = InstallHistoryEntry(
            id = UUID.randomUUID().toString(),
            startedAtMillis = logFile.lastModified().takeIf { it > 0L } ?: now,
            completedAtMillis = now,
            result = if (succeeded) InstallRunResult.Succeeded else InstallRunResult.Failed,
            log = buildString {
                appendLine("[F956B DZG3 test log imported after app start]")
                appendLine("source=$TEST_LOG_FILE")
                appendLine("sha256=$digest")
                appendLine()
                append(raw)
            },
            profileId = TEST_PROFILE_ID,
            usedShizuku = false,
        )
        InstallHistoryStore(this).save(entry)
        preferences.edit().putString(LAST_IMPORTED_SHA256, digest).commit()
    }

    companion object {
        private const val TEST_LOG_FILE = "f956b-dzg3-exploit.log"
        private const val TEST_PROFILE_ID = "q6q-F956BXXS4DZG3-exploit-test"
        private const val IMPORT_STATE = "f956b_test_log_import"
        private const val LAST_IMPORTED_SHA256 = "last_sha256"
    }
}
