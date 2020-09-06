import os
import shutil
import sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)))
import hpms_utils


def backup(output_path):
    import os
    if not os.path.isdir(output_path):
        return
    from datetime import datetime
    today = str(datetime.today().strftime('%Y%m%d%H%M%S'))
    bak_scripts_path = output_path + "_" + today
    shutil.make_archive(bak_scripts_path, 'zip', output_path)
    import hpms_utils
    hpms_utils.debug("Last project build backup done")


def unzip_templates(output_path):
    shutil.unpack_archive(hpms_utils.get_current_dir() + "/templates/data.zip", output_path, 'zip')


def create_empty_project(output_path):
    hpms_utils.debug("Creating default project template.")
    if os.path.isdir(output_path):
        shutil.rmtree(output_path, ignore_errors=True)
    os.makedirs(output_path)
    unzip_templates(output_path)


def main():
    import datetime
    try:
        print("\n\n\n---------------------------------------------")
        print("----------------- STARTED -------------------")
        print("---------------------------------------------\n")
        hpms_utils.system("HPMS batch starting")
        starting = datetime.datetime.now()
        start()
        ending = datetime.datetime.now() - starting
        hpms_utils.system("HPMS batch completed successfully in " + str(ending.total_seconds()) + " seconds")
        print("\n---------------------------------------------")
        print("----------------- FINISHED ------------------")
        print("---------------------------------------------\n\n\n")
    except Exception as e:
        hpms_utils.severe("Unexpected error: " + str(e))
        hpms_utils.system("HPMS batch aborted")
        print("\n---------------------------------------------")
        print("----------------- ABORTED -------------------")
        print("---------------------------------------------\n\n\n")


def start():
    import argparse

    argv = sys.argv

    if "--" not in argv:
        argv = []
    else:
        argv = argv[argv.index("--") + 1:]

    usage_text = (
            "Run HPMS project builder with this script:"
            "  blender --background --python " + __file__ + " -- [options]"
    )

    parser = argparse.ArgumentParser(description=usage_text)

    parser.add_argument(
        "-v", "--logging-level", dest="logging",
        help="Setting logging level (severe if not specified).",
    )

    parser.add_argument(
        "-o", "--output", dest="output_path", metavar='FILE',
        help="Generate HPMS into specified output path.",
    )

    parser.add_argument(
        "-c", "--cleanup", dest="cleanup",
        help="Cleanup the output directory (update otherwise).",
    )

    parser.add_argument(
        "-r", "--render", dest="render",
        help="Render missing screens and masks.",
    )

    parser.add_argument(
        "-l", "--roomupdate-list", dest="roomupdate_list",
        help="Force update for rooms in given list (comma separated).",
    )

    parser.add_argument(
        "-a", "--roomupdate-all", dest="roomupdate_all",
        help="Force update for all rooms.",
    )

    parser.add_argument(
        "-p", "--preview", dest="preview",
        help="Improve rendering speed with only 16 samples.",
    )

    args = parser.parse_args(argv)

    if not argv:
        parser.print_help()
        return

    hpms_utils.set_log_level(args.logging)

    if not args.output_path:
        hpms_utils.severe("Parameter '--outputpath' is missing, aborting")
        parser.print_help()
        return

    if not os.path.isdir(args.output_path):
        create_empty_project(args.output_path)
    else:
        backup(args.output_path)

    if args.cleanup is not None and args.cleanup.lower() in ["t", "true", "y", "yes"]:
        hpms_utils.debug("Re-building project.")
        create_empty_project(args.output_path)

    update_all = args.roomupdate_all is not None and args.roomupdate_all.lower() in ["t", "true", "y", "yes"]
    do_render = args.render is not None and args.render.lower() in ["t", "true", "y", "yes"]
    preview = args.preview is not None and args.preview.lower() in ["t", "true", "y", "yes"]
    room_list = []
    if args.roomupdate_list is not None:
        room_list = args.roomupdate_list.split(",")
    import hpms_exporter
    hpms_exporter.export_room_data(args.output_path, room_list, update_all, do_render, preview)


if __name__ == "__main__":
    main()
