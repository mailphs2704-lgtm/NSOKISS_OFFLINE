# NSOKISS Offline J2ME

This module is the target for the final one-install APK: a J2ME-compatible runtime containing the V7 client and the NSOKISS game runtime.

## Final architecture

The APK must contain:

- J2ME runtime/compatibility layer
- V7 client resources/classes
- NSOKISS gameplay runtime adapted for the J2ME environment
- game data
- device-local save storage

The final game must NOT require:

- an Internet server
- server discovery
- a separate NSOKISS server process
- MySQL/MariaDB installation
- a localhost server process

## Integration rule

The current NSOKISS server source remains the authoritative source for gameplay rules and world state. Network packet boundaries are to be replaced by an in-process bridge where the V7 client can call the adapted game runtime directly.

The supplied V7 JAR is binary/obfuscated and has no Java source. Therefore the repository does not pretend that the JAR has been converted to source. The binary must be treated as the rendering/input client artifact while the integration layer is built around its observable J2ME APIs and protocol behavior.

## Storage

The server's MySQL persistence layer is not part of the final APK. Player state will be mapped to a device-local record store/database appropriate to the J2ME runtime.

## Build stages

1. Reconstruct the V7 client entry/runtime contract.
2. Define the in-process client/runtime bridge.
3. Port only the NSOKISS runtime classes required by the client into J2ME-compatible Java.
4. Replace SQL persistence with device-local storage.
5. Bundle V7 + runtime + game data into the J2ME application.
6. Wrap the result in the selected Android J2ME runtime and produce the single APK.
