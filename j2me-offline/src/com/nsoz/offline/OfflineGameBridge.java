package com.nsoz.offline;

/**
 * Runtime boundary for the eventual J2ME-integrated game.
 * Network transport must not be required by this API.
 */
public final class OfflineGameBridge {
    private OfflineGameBridge() {}

    public static void start() {
        LocalGameState.load();
    }

    public static void shutdown() {
        LocalGameState.save();
    }
}
