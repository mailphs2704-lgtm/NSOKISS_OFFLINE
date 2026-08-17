# In-process V7 ↔ NSOKISS integration

## Current server boundary

`NSOKISS` currently exposes gameplay through network/session handling and persists through server-side database access.

## Offline boundary

The final J2ME game removes that process boundary:

```text
V7 MIDlet
  -> OfflineGameBridge
      -> player/session state
      -> map/zone/mob logic
      -> item/skill/task logic
      -> persistence adapter
```

There is no TCP endpoint in the final runtime.

## Compatibility strategy

Do not rewrite gameplay rules from scratch. Keep the existing NSOKISS classes as the reference implementation and progressively extract/adapt the smallest dependency graph needed by the V7 client.

For each client operation:

1. Identify the V7 packet/message.
2. Locate the corresponding NSOKISS handler.
3. Separate gameplay state mutation from socket/session code.
4. Move the gameplay mutation behind `OfflineGameBridge`.
5. Replace SQL reads/writes with local-storage calls.
6. Keep rendering/input behavior in the V7 client unchanged.

## First extraction targets

- login/local profile creation
- character load/save
- map entry and movement
- mob state and combat
- inventory/item state
- NPC/dialogue actions
- task state
- character progression

## Explicit non-goals

The offline build must not retain online server discovery, public server selection, external authentication, or a requirement to start a separate Java server.