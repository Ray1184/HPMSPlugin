import hpms_sector_data
import hpms_entity_data

bl_info = {
    "name": "HPMS Tools",
    "description": "Tools collection for HPMS maps.",
    "author": "Ray1184",
    "version": (1, 0),
    "location": "Object Properties",
    "blender": (2, 80, 0),
    "category": "Object",
    "wiki_url": "https://github.com/Ray1184/HPMSPlugin",
    "tracker_url": "https://github.com/Ray1184/HPMSPlugin",
}


def register():
    hpms_sector_data.register()
    hpms_entity_data.register()


def unregister():
    hpms_entity_data.unregister()
    hpms_sector_data.unregister()


if __name__ == "__main__":
    register()
