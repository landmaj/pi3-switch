import argparse
import logging
import sys

import i3ipc
import pynput

logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(
        description="Activates i3 workspace on the focused output. "
        "If there are two outputs, current workspace will "
        "be moved to the second (not focuses) output."
    )
    parser.add_argument("workspace", type=str, help="name of the i3 workspace")
    args = parser.parse_args()
    new_workspace = args.workspace

    try:
        i3 = i3ipc.Connection()
    except Exception as exc:
        logger.error("Could not connect to i3: {}".format(exc))
        sys.exit(1)

    outputs = [output for output in i3.get_outputs() if output["active"] is True]
    workspaces = [workspace["name"] for workspace in i3.get_workspaces()]

    if len(outputs) == 2 and len(workspaces) > 1:
        swap_two(i3, outputs, new_workspace)
    else:
        i3.command("workspace {}".format(args.workspace))


def swap_two(i3, outputs, new_workspace):
    mouse = pynput.mouse.Controller()
    cursor_position = mouse.position

    current_output = get_current_output(mouse.position, outputs)
    for output in outputs:
        if output["name"] == current_output:
            current_workspace = output["current_workspace"]

    if new_workspace == current_workspace:
        sys.exit(0)

    outputs = [output["name"] for output in outputs]
    outputs.remove(current_output)
    second_output = outputs[0]

    if not is_workspace_empty(i3, current_workspace):
        i3.command("move workspace to {}".format(second_output))

    i3.command(
        "[workspace={}] move workspace to {}".format(new_workspace, current_output)
    )
    i3.command("workspace {}".format(new_workspace))
    mouse.position = cursor_position


def is_workspace_empty(i3, current_workspace):
    """
    Returns True if workspace_name does not have any containers.
    """

    workspaces = [con for con in i3.get_tree() if con.type == "workspace"]
    for workspace in workspaces:
        if workspace.name == current_workspace and len(workspace.descendents()) == 0:
            return True
    return False


def get_current_output(mouse_position, outputs):
    """
    Returns currently focused output based on the cursor position.
    """

    for output in outputs:
        width = output["rect"]["width"]
        height = output["rect"]["height"]
        width_offset = output["rect"]["x"]
        height_offset = output["rect"]["y"]

        if width_offset == 0 and height_offset == 0:
            if (
                width_offset <= mouse_position[0] <= width_offset + width
                and height_offset <= mouse_position[1] <= height_offset + height
            ):
                return output["name"]
        elif width_offset == 0:
            if (
                width_offset <= mouse_position[0] <= width_offset + width
                and height_offset < mouse_position[1] <= height_offset + height
            ):
                return output["name"]
        elif height_offset == 0:
            if (
                width_offset < mouse_position[0] <= width_offset + width
                and height_offset <= mouse_position[1] <= height_offset + height
            ):
                return output["name"]
        else:
            if (
                width_offset < mouse_position[0] <= width_offset + width
                and height_offset < mouse_position[1] <= height_offset + height
            ):
                return output["name"]


if __name__ == "__main__":
    main()
