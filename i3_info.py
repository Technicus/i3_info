#!/bin/python

# https://i3ipc-python.readthedocs.io/en/latest/
# https://www.programcreek.com/python/example/97370/i3ipc.Connection

from json import dumps
from os import system
from i3ipc.aio import Connection
from i3ipc import Event
import asyncio
from ast import literal_eval
import io
from contextlib import redirect_stdout
#import sys
from subprocess import check_output


def clear():
    system("clear")

def get_current_workspace():
    workspace = check_output("i3-msg -t get_workspaces   | jq '.[] | select(.focused==true).name' | cut -d'\"' -f2", shell=True)
    workspace = str(workspace).strip("b'").rstrip("/\/n")
    return workspace

# Define a callback to be called when you switch workspaces.
async def on_workspace_focus(i3, event):
    # The first parameter is the connection to the ipc and the second is an object
    # with the data of the event sent from i3.

    # Capture event data.
    i3_ipc_event_data = event.ipc_data
    # Convert into JSON:
    i3_ipc_event_data_formatted = dumps(i3_ipc_event_data, indent=2)

    # Writing data to a file
    with open("./i3_info_on_workspace_focus.cache", "w") as cache_file:
        cache_file.write(f"{i3_ipc_event_data_formatted}\n")

    if event.current:
        print(f"on_workspace_focus(i3, event):\n  {event}")
        #for window in event.current.leaves():
            #print(f"event:\n  {window.name}")
            #print(f"event:\n  {event}\n")


# Report event and tree information
async def on_window_focus(i3, event):
    #tree = await i3.get_tree()
    workspaces = await i3.get_workspaces()
    outputs = await i3.get_outputs()

    # Capture event data.
    i3_ipc_event_data = event.ipc_data
    # Convert into JSON:
    i3_ipc_event_data_formatted = dumps(i3_ipc_event_data, indent=2)


    # Writing data to a file
    with open("./i3_info_window.cache", "w") as cache_file:
        cache_file.write(f"{i3_ipc_event_data_formatted}\n")

    # Parse data into variables
    window_output = str(i3_ipc_event_data["container"]["output"])
    # focused = tree.find_focused()
    # window_workspace = focused.workspace()

    # window_workspace = get_current_workspace()

    window_workspace = await i3.get_tree().find_focused().workspace().name

    window_container_id = str(i3_ipc_event_data["container"]["id"])


    window_title = str(i3_ipc_event_data["container"]["window_properties"]["title"]).rsplit(' ', 1)[-1]
    window_instance = str(i3_ipc_event_data["container"]["window_properties"]["instance"]).rsplit(' ', 1)[-1]
    window_class = str(i3_ipc_event_data["container"]["window_properties"]["class"]).rsplit(' ', 1)[-1]
    window_id = str(i3_ipc_event_data["container"]["window"])
    window_type = str(i3_ipc_event_data["container"]["window_type"])
    window_marks = str(i3_ipc_event_data["container"]["marks"])
    rect = str(i3_ipc_event_data["container"]["rect"])
    deco_rect = str(i3_ipc_event_data["container"]["deco_rect"])
    window_rect = str(i3_ipc_event_data["container"]["window_rect"])
    window_geometery = str(i3_ipc_event_data["container"]["geometry"])

    # Clear the screen and print a report.
    clear()

    print(f"output: \t", end = '')
    for output in outputs:
        if window_output in output.name:
            print(f"[{output.name}] ", end = '')
        else:
            print(f" {output.name}  ", end = '')
    print(f"\nworkspace:\t", end = '')
    for workspace in workspaces:
        if str(window_workspace) in workspace.name:
            print(f"[{workspace.name}] ", end = '')
        else:
            print(f" {workspace.name}  ", end = '')
    print(f"\ncontainer_id:\t{window_container_id}")
    print(f"title:\t\t{window_title}")
    print(f"instance:\t{window_instance}")
    print(f"class:\t\t{window_class}")
    print(f"id:\t\t{window_id}")
    print(f"type:\t\t{window_type}")
    print(f"marks:\t\t{window_marks}")
    dimension = ''
    for key, value in literal_eval(rect).items():
        dimension += str(value) + ', '
    print(f"rect:\t\t({dimension.rstrip(', , ')})")
    dimension = ''
    for key, value in literal_eval(deco_rect).items():
        dimension += str(value) + ', '
    print(f"deco:\t\t({dimension.rstrip(', , ')})")
    dimension = ''
    for key, value in literal_eval(window_rect).items():
        dimension += str(value) + ', '
    print(f"window:\t\t({dimension.rstrip(', , ')})")
    dimension = ''
    for key, value in literal_eval(window_geometery).items():
        dimension += str(value) + ', '
    print(f"geometery:\t({dimension.rstrip(', , ')})\n")


async def binding_report(i3, event):
    # Report event and tree information
    binding = event.ipc_data["binding"]["command"].strip()
    print(f"binding:\n  {binding}\n")
    # Capture event data.
    i3_ipc_event_data = event.ipc_data
    # Convert into JSON:
    i3_ipc_event_data_formatted = dumps(i3_ipc_event_data, indent=2)
    # Writing data to a file
    with open("./i3_info_binding.cache", "w") as cache_file:
        cache_file.write(f"i3.on(Event.BINDING, binding_report):\n{i3_ipc_event_data_formatted}\n")
    return "test_complete"


async def main():
    i3 = await Connection(auto_reconnect=True).connect()
    #i3.on(Event.WINDOW_FOCUS, on_window_focus)
    i3.on(Event.WINDOW_FOCUS, on_window_focus)
    #i3.on(Event.WINDOW, on_window_focus)
    i3.on(Event.BINDING, binding_report)
    #i3.on(Event.WORKSPACE_FOCUS, on_workspace_focus)

    # Reading from file
    # with open("./i3_info.cache", "r+") as cache_file:
        ## Reading form a file
        #print(cache_file.read())

    await i3.main()


if __name__ == "__main__":
    clear()
    asyncio.new_event_loop().run_until_complete(main())
