# Client V7 Offline

This directory defines the offline target for the supplied J2ME V7 client (`V7_217_X1(1).jar`).

## Target runtime

The same V7 client must be usable from:

- MicroEmulator on Windows/Linux/macOS.
- A J2ME-compatible Android runtime/APK.

## Offline contract

The final client must:

1. Never download a server list from the Internet.
2. Never select an online server.
3. Connect only to the local NSOKISS runtime endpoint.
4. Use the offline game protocol already implemented by NSOKISS.
5. Persist player data locally on the device.

The supplied V7 JAR is obfuscated and contains 828 files/classes/resources. Its `GameMidlet` already contains port `14444`. The client-side server discovery code is therefore the part that must be removed/replaced; the game protocol itself should remain compatible with NSOKISS.

## Important implementation note

The JAR is a binary attachment and is not rewritten through the text-only GitHub Contents API. The repository therefore contains the reproducible patching/build instructions rather than pretending that a binary JAR has already been committed.

The patch process must operate on the exact supplied JAR and produce a new JAR with the same resources/classes except for the server-discovery path.
