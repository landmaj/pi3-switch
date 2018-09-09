import argparse
import logging
import sys

import i3ipc
import pynput

logger = logging.getLogger(__name__)


class WorkspaceSwitcher:
    def __init__(self, args):
        try:
            self.i3 = i3ipc.Connection()
        except Exception as exc:
            logger.error("Could not connect to i3: {}".format(exc))
            sys.exit(1)

        self.args = args

        self.workspaces = [workspace for workspace in self.i3.get_workspaces()]
        self.outputs = [
            output for output in self.i3.get_outputs() if output["active"] is True
        ]

        self.mouse = pynput.mouse.Controller()
        self.mouse_position = self.mouse.position

        self.new_workspace_name = args.workspace
        if args.focus:
            self.current_output_name = self._get_output_from_focused_window()
        else:
            self.current_output_name = self._get_output_from_cursor_position()

    def _restore_cursor_position(self):
        self.mouse.position = self.mouse_position

    def _is_workspace_on_current_output(self):
        for workspace in self.workspaces:
            if workspace.name == self.new_workspace_name:
                return workspace["output"] == self.current_output_name
        return False

    def _is_workspace_occupied(self, current_workspace_name):
        workspaces = [con for con in self.i3.get_tree() if con.type == "workspace"]
        for workspace in workspaces:
            if (
                workspace.name == current_workspace_name
                and len(workspace.descendents()) == 0
            ):
                return False
        return True

    def _get_output_from_focused_window(self):
        workspace_name = self.i3.get_tree().find_focused().workspace().name
        for output in self.outputs:
            if output["current_workspace"] == workspace_name:
                return output["name"]

    def _get_output_from_cursor_position(self):
        for output in self.outputs:
            width = output["rect"]["width"]
            height = output["rect"]["height"]
            x_offset = output["rect"]["x"]
            y_offset = output["rect"]["y"]

            if x_offset == 0 and y_offset == 0:
                if (
                    x_offset <= self.mouse_position[0] <= x_offset + width
                    and y_offset <= self.mouse_position[1] <= y_offset + height
                ):
                    return output["name"]
            elif x_offset == 0:
                if (
                    x_offset <= self.mouse_position[0] <= x_offset + width
                    and y_offset < self.mouse_position[1] <= y_offset + height
                ):
                    return output["name"]
            elif y_offset == 0:
                if (
                    x_offset < self.mouse_position[0] <= x_offset + width
                    and y_offset <= self.mouse_position[1] <= y_offset + height
                ):
                    return output["name"]
            else:
                if (
                    x_offset < self.mouse_position[0] <= x_offset + width
                    and y_offset < self.mouse_position[1] <= y_offset + height
                ):
                    return output["name"]

    def simple_switch(self):
        # If the selected workspace does not exist or is already on the
        # current output, do not move it. This also catches the case
        # if there is only one output.
        if (
            self.new_workspace_name in [ws["name"] for ws in self.workspaces]
            and not self._is_workspace_on_current_output()
        ):
            self.i3.command(
                "[workspace={}] move workspace to {}".format(
                    self.new_workspace_name, self.current_output_name
                )
            )
        self.i3.command("workspace {}".format(self.new_workspace_name))

        self._restore_cursor_position()
        sys.exit(0)

    def push_to_secondary(self, master_only=False):
        # this method only works for two outputs
        if len(self.outputs) != 2:
            self.simple_switch()

        for output in self.outputs:
            if output["name"] == self.current_output_name:
                current_workspace_name = output["current_workspace"]

        if self.new_workspace_name == current_workspace_name:
            sys.exit(0)

        for output in self.outputs:
            if output["name"] != self.current_output_name:
                second_output = output["name"]
                secondary_is_master = output["primary"]
                break

        # Do not move current workspace if it is empty to avoid pushing
        # newly created workspaces around or if master-slave is enabled.
        if self._is_workspace_occupied(current_workspace_name) and not (
            secondary_is_master and master_only
        ):
            self.i3.command("move workspace to {}".format(second_output))

        # We can skip moving workspace and avoid flickering if
        # it is already on that output.
        if not self._is_workspace_on_current_output():
            self.i3.command(
                "[workspace={}] move workspace to {}".format(
                    self.new_workspace_name, self.current_output_name
                )
            )

        self.i3.command("workspace {}".format(self.new_workspace_name))

        self._restore_cursor_position()
        sys.exit(0)

    def swap(self):
        raise NotImplementedError

    def switch_workspace(self):
        if self.args.master:
            self.push_to_secondary(master_only=True)
        elif self.args.push:
            self.push_to_secondary()
        elif self.args.swap:
            self.swap()
        else:
            self.simple_switch()


def main():
    parser = argparse.ArgumentParser(
        description="Moves selected i3 workspace to the current output "
        "(by default determined by cursor location) and focuses it."
    )

    parser.add_argument("workspace", type=str, help="name of the i3 workspace")
    parser.add_argument(
        "-f",
        "--focus",
        action="store_true",
        help="use focused window instead of cursor "
        "position to determine the current output",
    )

    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "-p",
        "--push",
        action="store_true",
        help="moves replaced workspace to the second output "
        "(works only if there are two outputs, ignored otherwise)",
    )
    group.add_argument(
        "-m",
        "--master",
        action="store_true",
        help="same as 'push' but will only move from "
        "primary output to the secondary",
    )
    group.add_argument(
        "-s",
        "--swap",
        action="store_true",
        help="(NOT IMPLEMENTED YET) behaves like xmonad, swaps workspaces "
        "if they are on a different output",
    )

    args = parser.parse_args()
    WorkspaceSwitcher(args).switch_workspace()


if __name__ == "__main__":
    main()
