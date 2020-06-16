from collections import defaultdict


class HPMSShared:
    cams_by_sector_by_room = None
    room_by_sector = None

    def __init__(self):
        self.cams_by_sector_by_room = defaultdict(dict)
        self.room_by_sector = dict()

    def put_room(self, sector, room):
        self.room_by_sector[sector] = room

    def put_cam(self, room, sector, cam):
        self.cams_by_sector_by_room[room][sector] = cam

    def get_room_by_sector(self, sector):
        if sector in self.room_by_sector:
            return self.room_by_sector[sector]
        return "None"

    def get_cam_by_sector_and_room(self, room, sector):
        if room in self.cams_by_sector_by_room and sector in self.cams_by_sector_by_room[room]:
            return self.cams_by_sector_by_room[room][sector]
        return "None"
