from typing import List, Dict, Tuple
from dataclasses import dataclass, field
from classes.connection import Connection
from classes.hub import Hub
from classes.map import Map
import re


class ParserError(Exception):
    pass


@dataclass
class ParsedData:
    hubs: dict[str, Hub]
    cons: dict[str, Connection]
    start: Hub | None
    end: Hub | None
    nb_drones: int = 0
    


class Parser:
    DUP = {'hub', 'connection'}
    UNIQUE = {'nb_drones', 'start_hub', 'end_hub'}
    REQ = UNIQUE | DUP

    def __init__(self, map: str) -> None:
        self.map = map
        self.data = ParsedData({}, {}, None, None, 0)
        
    def parse(self):
        self.read_map()
        return Map(self.data.hubs, self.data.cons,
                   self.data.start, self.data.end, self.data.nb_drones)

    def read_map(self) -> Dict:
        try:
            with open(self.map) as f:
                i = 0
                found_keys = []
                found_vals = []
                for no, raw in enumerate(f, start=1):
                    line = raw.strip()
                    if not line or line.startswith("#"):
                        continue
                    if ':' not in line or line.split(':')[0].lower() not in self.REQ:
                        raise ParserError(f"line {no}: "
                                            "Unknown line format or key!")
                    if '#' in line:
                        line = line.split('#')[0]
                    if i == 0 and line.split(':')[0].lower() != 'nb_drones':
                        raise ParserError(f"line {no}: "
                                          "map should start with 'nb_drones' key!")
                    key = line.split(":")[0].lower().strip()
                    val = line.split(":")[1].lower().strip()
                    if key in self.UNIQUE and key in found_keys:
                        raise ParserError(f"line {no}: "
                                          f"keys {self.UNIQUE} must be unique!")
                    found_keys.append(key)
                    if val in found_vals:
                        raise ParserError(f"line {no}: "
                                          "Duplicates are forbiden!")
                    found_vals.append(val)
                    if key == 'nb_drones':
                        self.parse_nb_drones(val, no)
                    if key == 'hub':
                        self.parse_hub(val, no, False, False)
                    if key == 'start_hub':
                        self.parse_hub(val, no, True, False)
                    if key == 'end_hub':
                        self.parse_hub(val, no, False, True)
                    if key == 'connection':
                        self.parse_connections(val, no)
                    if i == 0:
                        i += 1

        except OSError as e:
            raise ParserError(e)
        except IsADirectoryError as e:
            raise ParserError(e)
        except FileNotFoundError as e:
            raise ParserError(e)

    def parse_nb_drones(self, val: str, no: int):
        try:
            v = int(val)
            if v < 0:
                raise ParserError(f"line {no}: 'nb_drones' must be +int!")
            self.data.nb_drones = v
        except Exception:
            raise ParserError(f"line {no}: 'nb_drones' must be +int!")

    def parse_hub(self, val: str, no: int, start: bool, end: bool):
            zone, max_drones, color = 'normal', 1, None
            if val.count('[') != val.count(']'):
                raise ParserError(f"line {no}: Invalid brackets!")
            p = val.split("[", maxsplit=1)
            if '[' in val and ']' in val:
                if len(p[0].strip().split(' ')) != 3 or p[1].strip().split(']')[1]:
                    raise ParserError(f"line {no}: Unknown line format!")
                cont = p[1].strip().lstrip('[ ').rstrip('] ')
                if not cont:
                    color = None
                    max_drones = 1
                    zone = 'normal'
                else:
                    pairs = dict(self.check_metadata(cont, no, key='hub'))
                    color = pairs.get("color", None)
                    max_drones = int(pairs.get("max_drones", 1))
                    zone = pairs.get("zone", 'normal')
            else:
                if len(val.strip().split(' ')) != 3:
                    raise ParserError(f"line {no}: Unknown line format!")
            if (start or end):
                max_drones = float('inf')
            data = self.get_hub_data(p[0].lower().strip(), no)
            self.validate_after_parsing(data, no, key='hub')
            name = data['name']
            if '-' in name:
                raise ParserError(f"line {no}: Dashes are forbidden!")
            x = data['x']
            y = data['y']
            s = start if start else False
            e = end if end else False
            h = Hub(name, x, y, zone, color, max_drones, s, e, 0, )
            if start:
                self.data.start = h
            if end:
                self.data.end = h
            self.data.hubs[name] = h

    def parse_connections(self, val: str, no: int):
        p, mlc = val.split("[", maxsplit=1), 1
        if '[' in val and ']' in val:
            if len(p[0].strip().split('-')) != 2 or p[1].split(']')[1]:
                raise ParserError(f"line {no}: Invalid line format!!")
            cont = p[1].strip().lstrip('[ ').rstrip('] ').lower()
            if not cont:
                mlc = 1
            else:
                mlc = self.check_metadata(cont, no, key="connection")
        else:
            if len(val.strip().split('-')) != 2 or ' ' in val.strip():
                raise ParserError(f"line {no}: Invalid line format!!")
        connect = self.get_connection_data(p[0].lower().strip(), no)
        self.validate_after_parsing(p[0].lower(), no, key='connection')
        hub_a = self.data.hubs.get(connect[0])
        hub_b = self.data.hubs.get(connect[1])
        c = Connection(hub_a, hub_b, mlc, [])
        self.data.cons[p[0].lower()] = c

    def check_metadata(self, cont: str, no: int, key: str):
        METADATA = {'', 'max_drones', 'color', 'zone'}
        TYPES = {'normal', 'restricted', 'priority', 'blocked'}
        if key == 'connection':
            p = cont.lower().split('=')
            if 'max_link_capacity' not in cont.lower():
                raise ParserError(f"line {no}: "
                                  "metadata for connections must be: "
                                  "[max_link_capacity=value].")
            elif len(p) != 2 or p[0].strip() != 'max_link_capacity':
                raise ParserError(f"line {no}: "
                                  "metadata for connections must be: "
                                  "[max_link_capacity=value].")
            else:
                try:
                    mlc = int(p[1])
                    if mlc <= 0:
                        raise ParserError(f"line {no}: "
                                          "max_link_capacity must be +int.")
                    return mlc
                except Exception:
                    raise ParserError(f"line {no}: "
                                      "max_link_capacity must be +int.")
        elif key == 'hub':
            pattern = r"(\S+)\s*=\s*(\S+)"
            pairs = re.findall(pattern, cont)
            k1 = any(w in cont.lower() for w in METADATA if w)
            k2 = [w for w in METADATA if cont.lower().count(w) > 1 and w]
            if '=' not in cont or not k1 or cont.count('=') > 3:
                raise ParserError(f"line {no}: "
                                  "Invalid metadata.\n"
                                  "e.g: [color=val zone=val max_drones=val].")
            elif k2:
                raise ParserError(f"line {no}: "
                                  "Duplicates are forbidden!")
            else:
                for key, val in pairs:
                    if key not in METADATA:
                        raise ParserError(f"line {no}: "
                                          f"invalid key {key}.")
                    if key == 'zone' and val not in TYPES:
                        raise ParserError(f"line {no}: "
                                          "Invalid zone type.")
                    if key == 'color' and not val.isalpha():
                        raise ParserError(f"line {no}: "
                                          "Invalid color.")
                    if key == 'max_drones':
                        try:
                            int(val)
                        except Exception:
                            raise ParserError(f"line {no}: "
                                              "max_drones must be +int.")
                return pairs

    def get_hub_data(self, cont: str, no: int):
        p = cont.split(' ')
        if len(p) != 3 or any(1 for i in p if not i):
            raise ParserError(f"line {no}: "
                              "Invalid hub format! "
                              "expected: 'name x y [metadata]'.")
        try:
            x = int(p[1])
            y = int(p[2])
            return {'name': p[0], 'x': x, 'y': y}
        except ValueError:
            raise ParserError(f"line {no}: "
                              "coordinates must be integers.")
        
    def get_connection_data(self, cont: str, no: int):
        if '-' not in cont:
                raise ParserError(f"line {no}: Invalid connection!"
                                  "\nexpected: zone1-zone2.")
        else:
            p = cont.split('-')
            if len(p) != 2 or not p[0] or not p[1]:
                raise ParserError(f"line {no}: Invalid connection!"
                                  "\nexpected: zone1-zone2.")
            else:
                return p[0], p[1]

    def validate_after_parsing(self, cont: str | dict, no: int, key: str):
        if key == 'connection':
            cont = cont.strip()
            a, b = [i.strip() for i in cont.split('-')]
            for k in self.data.cons.keys():
                if sorted([i.strip() for i in cont.split('-')]) == sorted([i.strip() for i in k.split('-')]):
                    raise ParserError(f"line {no}: duplicated connection!")
            if any(i not in self.data.hubs.keys() for i in (a, b)):
                raise ParserError(f"line {no}: Unknown hub(s) in connection {cont}.")
        if key == 'hub':
            if cont['name'] in self.data.hubs:
                raise ParserError(f"line {no}: hub must be unique!")
            for h in self.data.hubs.values():
                if h.x == cont['x'] and h.y == cont['y']:
                    raise ParserError(f"line {no}: "
                                      "2 hubs cannot have same coordinates.")
