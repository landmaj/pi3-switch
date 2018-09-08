import argparse
import logging
import sys

import i3ipc

logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(
        description="Activates i3 workspace on the focused output. "
                    "If there are two outputs, current workspace will "
                    "be moved to the second (not focuses) output."
    )
    parser.add_argument('workspace', type=str, help="name of the i3 workspace")
    args = parser.parse_args()
    new_workspace = args.workspace

    try:
        i3 = i3ipc.Connection()
    except Exception as exc:
        logger.error("Could not connect to i3: {}".format(exc))
        sys.exit(1)

    outputs = [
        output["name"] for output in i3.get_outputs()
        if output["active"] is True
    ]
    workspaces = [workspace['name'] for workspace in i3.get_workspaces()]

    if new_workspace not in workspaces:
        logger.warning("Workspace '{}' does not exist".format(new_workspace))
        sys.exit(1)

    if len(outputs) == 2 and len(workspaces) > 1:
        swap_two_screen(i3, outputs, new_workspace)
    else:
        i3.command("workspace {}".format(args.workspace))


def swap_two_screen(i3, outputs, new_workspace):
    for workspace in i3.get_workspaces():
        if workspace['focused'] is True:
            old_workspace = workspace
            break
    active_output = old_workspace["output"]

    outputs.remove(active_output)
    second_output = outputs.pop()

    if new_workspace == old_workspace['name']:
        sys.exit(0)

    i3.command(
        "[workspace={}] move workspace to {}"
        .format(old_workspace["name"], second_output))
    i3.command(
        "[workspace={}] move workspace to {}"
        .format(new_workspace, active_output)
    )

    i3.command("workspace {}".format(old_workspace["name"]))
    i3.command("workspace {}".format(new_workspace))


if __name__ == "__main__":
    main()
