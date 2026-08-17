# NSOKISS Offline conversion

This branch is the offline-conversion work tree for NSOKISS.

## Current architecture

- Game server source is local in this repository.
- Game data is local in `Data/`.
- Server listens on a local game port from `config.properties`.
- MySQL and MongoDB endpoints are configured to loopback by default.
- `run.bat` builds and starts the local server.

## Important

The current source still uses JDBC/MySQL as its persistence layer. This means a completely self-contained offline package still requires the database layer to be replaced or bundled locally. The conversion must not claim to be complete until player data can be created, loaded and saved without any external machine.

## Conversion milestones

1. [x] Copy complete NSOKISS source/data into this repository.
2. [x] Create isolated `offline-conversion` branch.
3. [x] Add local server configuration.
4. [x] Add local build verification workflow.
5. [ ] Remove external database dependency and provide embedded local persistence.
6. [ ] Make client connection point to the local server.
7. [ ] Add one-click launcher for server + client.
8. [ ] Produce a distributable Windows package.
