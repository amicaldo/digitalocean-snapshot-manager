# DOSM (DigitalOcean Snapshot Manager)

**DOSM** is a snapshot scheduling library for DigitalOcean volumes.

## Usage
To use **DOSM** you need to have a **.yaml** config file prepared.
This config file contains settings - your DigitalOcean API key for instance - and a list of your volumes:

```yaml
settings:
    digitalocean:
        api_key: your_digitalocean_api_key

volumes:
-   name: 'volume_00001'
    rules:
    - 168
    - 720
    uuid: 226h1ajk1c58gicn54hngekgd6k1becj9j0g0joa
-   ...
```

The `settings` section - or the DigitalOcean API key respectively - must be provided by default.

The `volumes` section is created automatically if not provided.
By using the `SnapshotManager` you're able to add, list and remove volume entries.

The `rules` section of the volume entries is a list of *hours* in which snapshots should be taken.

## API Example
```python
from dosm import SnapshotManager

snapman: object = SnapshotManager(
    config_path='/path/to/config.yml',
    log_path='/path/to/dosm.log'
)

# Get all volumes from DigitalOcean
volumes: list = snapman.list_volumes()

# Get all volume entries from your config.yml
entries: list = snapman.list_volume_entries()

# Add volume entry
snapman.add_volume_entry(
    name=volumes[0].name,
    uuid=volumes[0].uuid,
    rules=[12, 24]
)

# Remove volume entry
snapman.remove_volume_entry_by_uuid(uuid=volumes[0].uuid)

# Start the main loop every 30 minutes (1800 seconds)
snapman.run(interval=1800)
```

# Author
Jannik Hauptvogel - amicaldo GmbH - hauptvogel@amicaldo.de
