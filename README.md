# minecraft-server-wizard

I run a few local Minecraft servers for testing plugins and playing with friends. Setting them up manually every time (downloading the jar, writing the startup batch file with proper flags, accepting the EULA, and modifying properties) got tedious. This is a simple CLI to bootstrap a server directory in seconds.

It handles downloading the latest stable build of Paper or Vanilla, generates a `run.bat` with optimized JVM flags (Aikar's flags), accepts the EULA, and lets you set common properties directly from the command line without destroying comments in your existing `server.properties` file.

## Installation

Clone the repository and install the dependencies:

```cmd
git clone https://github.com/example/minecraft-server-wizard.git
cd minecraft-server-wizard
pip install -r requirements.txt
```

## How to use

To bootstrap a new Paper server for version 1.20.4 in the current directory:

```cmd
python wizard.py init --type paper --version 1.20.4 --memory 4G
```

This will:
1. Query the Paper MC API for the latest stable build of 1.20.4.
2. Download the JAR directly to the directory.
3. Create `eula.txt` with `eula=true`.
4. Create a Windows launch script `run.bat` configured with 4 gigabytes of RAM and Aikar's garbage collection flags.

You can also update configuration values without opening the properties file:

```cmd
python wizard.py config --set motd="My Test Server" --set server-port=25575 --set view-distance=10
```

<!-- verified: 2026-09-15 -->
