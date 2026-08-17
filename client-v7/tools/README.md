# V7 JAR patching

The supplied `V7_217_X1(1).jar` is an obfuscated J2ME binary. The repository cannot safely rewrite that binary through the text-only GitHub Contents API, so the patch is reproducible from the exact JAR attachment.

The first offline patch target is the server-discovery URL stored in `S.class`. The client already has the game socket port `14444` in `GameMidlet`, so the final patch must make discovery local and deterministic rather than contacting an Internet server list.

## Final target

`S.class` must obtain only a local endpoint, and the selected game server must be:

- host: `127.0.0.1`
- port: `14444`

The patch must preserve all other classes/resources and the original J2ME MIDlet structure.

## Why this is separate from the server conversion

Making the client local is only one layer. The final one-file J2ME game also needs the NSOKISS runtime logic to be executable inside the target J2ME environment and a device-local save store. The server source currently depends on Java SE/MySQL infrastructure, so it cannot simply be copied into the MIDlet JAR and expected to run.
