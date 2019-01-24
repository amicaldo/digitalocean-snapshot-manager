import threading
from datetime import datetime, timedelta

from .confman import Confman
from .logger import Logger

from libcloud.compute.types import Provider
from libcloud.compute.providers import get_driver


class SnapshotManager:
    __time_format: str = '%Y-%m-%d_%H:%M:%S'

    def __init__(self, config_path: str, log_path: str = None):
        self.__confman: object = Confman(config_path=config_path)
        self.__logger: object = Logger(log_path=log_path) if log_path else None

        cls: any = get_driver(Provider.DIGITAL_OCEAN)

        self.__do_api: object = cls(
            self.__confman.get_digitalocean_api_key(),
            api_version='v2'
        )

    def __extract_snapshot_date(self, snapshot: object) -> object:
        parts: list = snapshot.name.split('_')

        return datetime.strptime('_'.join(parts[1::]), self.__time_format)

    def __validate_snapshot(self, snapshot: object) -> bool:
        try:
            date: object = self.__extract_snapshot_date(snapshot)

            return True

        except:
            return False

    def __amend_snapshot(self, snapshot: object) -> object:
        snapshot.created_at: object = self.__extract_snapshot_date(snapshot)

        return snapshot

    def __get_oldest_snapshot(self, snapshots: list) -> object:
        oldest: object = None

        for snapshot in snapshots:
            if not oldest or oldest.created_at > snapshot.created_at:
                oldest: object = snapshot

        return oldest

    def __get_newest_snapshot(self, snapshots: list) -> object:
        newest: object = None

        for snapshot in snapshots:
            if not newest or newest.created_at < snapshot.created_at:
                newest: object = snapshot

        return newest

    def __filter_snapshots_by_rules(self, snapshots: list, rules: list) -> dict:
        for rule in rules:
            delta: object = timedelta(hours=rule)

            later: list = [
                s for s in snapshots if (s.created_at + delta) >= self.__date_now
            ]

            if later:
                protected: object = self.__get_newest_snapshot(later)
            else:
                protected: object = self.__get_oldest_snapshot(snapshots)

            if protected:
                snapshots.remove(protected)

        return snapshots

    def __process_snapshots(self, entry: dict, volume: object, snapshots: list):
        if not entry['rules']:
            if self.__logger:
                self.__logger.warn('No rules specified for %s' % entry['name'])

            return

        entry['rules'].sort(reverse=True)

        newest: object = self.__get_newest_snapshot(snapshots)
        delta: object = timedelta(hours=entry['rules'][-1])

        if not newest or newest.created_at < datetime.now() - delta:
            name: str = '%s_%s' % (
                volume.name,
                datetime.now().strftime(self.__time_format)
            )

            if self.__logger:
                self.__logger.info('Creating snapshot for volume %s' % volume.name)

            snapshots.append(self.__amend_snapshot(
                snapshot=volume.snapshot(name=name)
            ))

        trash: list = self.__filter_snapshots_by_rules(
            snapshots=snapshots,
            rules=entry['rules']
        )

        for snapshot in trash:
            if self.__logger:
                self.__logger.info('Destroying snapshot %s' % snapshot.name)

            res: bool = self.__do_api.delete_volume_snapshot(snapshot=snapshot)

            if not res and self.__logger:
                self.__logger.error('Failed to destroy snapshot %s' % snapshot.name)

    def __process_volume(self, entry: dict, volume: object):
        snapshots: list = list(map(self.__amend_snapshot, [
            s for s in volume.list_snapshots() if self.__validate_snapshot(s)
        ]))

        if self.__logger:
            self.__logger.info('Found %d valid snapshots of volume %s' % (
                len(snapshots), volume.name
            ))

        self.__process_snapshots(
            entry=entry,
            volume=volume,
            snapshots=snapshots
        )

    def __process_entry(self, entry: dict):
        volume: object = next(
            (v for v in self.__volumes if v.uuid == entry['uuid']),
            None
        )

        if not volume:
            if self.__logger:
                self.__logger.warn('Could not find volume for entry %s' % entry['name'])
        else:
            self.__process_volume(entry=entry, volume=volume)

    def list_volumes(self) -> list:
        return self.__do_api.list_volumes()

    def list_volume_entries(self) -> list:
        return self.__confman.list_volume_entries()

    def add_volume_entry(self, name: str, uuid: str, rules: list):
        self.__confman.add_volume_entry(name=name, uuid=uuid, rules=rules)

    def remove_volume_entry_by_uuid(self, uuid: str):
        self.__confman.remove_volume_entry_by_uuid(uuid=uuid)

    def run(self, interval: int):
        threading.Timer(interval, self.run_once).start()

    def run_once(self):
        self.__date_now: object = datetime.now()
        self.__entries: list = self.__confman.list_volume_entries()
        self.__volumes: list = self.__do_api.list_volumes()

        if self.__logger:
            self.__logger.info('Found %d entries' % len(self.__entries))

        for entry in self.__entries:
            if self.__logger:
                self.__logger.info('Processing entry %s' % entry['name'])

            self.__process_entry(entry=entry)
