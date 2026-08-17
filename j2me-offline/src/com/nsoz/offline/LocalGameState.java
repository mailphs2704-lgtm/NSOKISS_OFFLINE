package com.nsoz.offline;

/** Placeholder for device-local persistence. The final J2ME port will use RecordStore. */
public final class LocalGameState {
    private LocalGameState() {}

    public static void load() {
        // J2ME RecordStore integration is added when the client runtime is ported.
    }

    public static void save() {
        // J2ME RecordStore integration is added when the client runtime is ported.
    }
}
