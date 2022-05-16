#!/bin/python

# https://i3ipc-python.readthedocs.io/en/latest/


import json
from os import system
from i3ipc.aio import Connection
from i3ipc import Event
import asyncio
from ast import literal_eval


def clear():
    system("clear")


# Define a callback to be called when you switch workspaces.
def on_workspace_focus(i3, event):
    # The first parameter is the connection to the ipc and the second is an object
    # with the data of the event sent from i3.
    if event.current:
        print(f"on_workspace_focus(i3, event):\n  {event}\n")
        #for window in event.current.leaves():
            #print(f"event:\n  {window.name}")
            #print(f"event:\n  {event}\n")


def on_window(i3, event):
    print(f"on_window():\n  {event}\n")

# Report event and tree information
async def binding_report(i3, event):
    binding = event.ipc_data["binding"]["command"].strip()
    #binding = event.ipc_data
    print(f"binding: {binding}\n")

# Report event and tree information
async def on_window_focus(i3, event):
    i3_tree = await i3.get_tree()
    workspaces = await i3.get_workspaces()
    outputs = await i3.get_outputs()
    # Capture event data.
    i3_ipc_event_data = event.ipc_data
    # Convert into JSON:
    i3_ipc_event_data_formatted = json.dumps(i3_ipc_event_data, indent=4)
    with open("./i3_info.cache", "w") as cache_file:
    # Writing data to a file
        #cache_file.write(f"event:\n  {event}\n\n")
        #cache_file.write(f"i3.get_tree():\n  {i3_tree}\n\n")
        cache_file.write(f"event.ipc_data():\n  {i3_ipc_event_data_formatted}\n")
    window_title = str(i3_ipc_event_data["container"]["window_properties"]["title"]).rsplit(' ', 1)[-1]
    window_instance = str(i3_ipc_event_data["container"]["window_properties"]["instance"]).rsplit(' ', 1)[-1]
    window_class = str(i3_ipc_event_data["container"]["window_properties"]["class"]).rsplit(' ', 1)[-1]
    window_type = str(i3_ipc_event_data["container"]["window_type"])
    window_marks = str(i3_ipc_event_data["container"]["marks"])
    rect = str(i3_ipc_event_data["container"]["rect"])
    deco_rect = str(i3_ipc_event_data["container"]["deco_rect"])
    window_rect = str(i3_ipc_event_data["container"]["window_rect"])
    window_geometery = str(i3_ipc_event_data["container"]["geometry"])
    window_id = str(i3_ipc_event_data["container"]["window"])
    window_container_id = str(i3_ipc_event_data["container"]["id"])
    window_output = str(i3_ipc_event_data["container"]["output"])
    focused = i3_tree.find_focused()
    window_workspace = focused.workspace()
    clear()
    print(f"output: {window_output}")
    print(f'workspace: {window_workspace.name}')
    print(f"container_id: {window_container_id}")
    print(f"title: {window_title}")
    print(f"instance: {window_instance}")
    print(f"class: {window_class}")
    print(f"id: {window_id}")
    print(f"type: {window_type}")
    print(f"marks: {window_marks}")
    dimension = ''
    for key, value in literal_eval(rect).items():
        dimension += str(value) + ', '
    print(f"rect: ({dimension.rstrip(', , ')})")
    dimension = ''
    for key, value in literal_eval(deco_rect).items():
        dimension += str(value) + ', '
    print(f"deco: ({dimension.rstrip(', , ')})")
    dimension = ''
    for key, value in literal_eval(window_rect).items():
        dimension += str(value) + ', '
    print(f"window: ({dimension.rstrip(', , ')})")
    dimension = ''
    for key, value in literal_eval(window_geometery).items():
        dimension += str(value) + ', '
    print(f"geometery: ({dimension.rstrip(', , ')})\n")

    #if event.ipc_data.has_key("binding"):
    if "binding" in event.ipc_data:
        binding = event.ipc_data["binding"]["command"].strip()
        #binding = event.ipc_data
        print(f"binding: {binding}\n")
    #else:

    # get some information about the focused window
    #print(f'Focused window: {focused.name}')
    #window_output = focused.output()
    #print(f'window_output: {window_output.name}')

    #print(f'outputs:')
    #for output in outputs:
        #print(f'  {output.name}')
    #print()
    #print(f'workspaces:')
    #for workspace in workspaces:
        #print(f'  {workspace.name}')
    #print()


    #print(f"keybind:{}")
    #print(f"action:{}")
    #print(f"window_workspace: {str(i3_tree.workspace)}\n")
    #print(f"\ni3_tree attributes:")
    #for attribute in dir(i3_tree):
        #if '__' not in attribute:
            #print(f"{attribute}")
    #print(f"\ntype(i3_tree.workspace): {type(i3_tree.workspace())}")
    #print(f"\ntype(i3_tree.workspace).__getattribute__: {i3_tree.workspace.__getattribute__}")
    #print(f"\ni3_tree.workspace attributes:")
    #for attribute in dir(i3_tree.workspace()):
        ##if '__' not in attribute:
        #print(f"{attribute}")
    #print(f"\ntype(i3_tree.workspaces): {type(i3_tree.workspaces())}")
    #print(f"\ni3_tree.workspaces attributes:")
    #for attribute in dir(i3_tree.workspaces()):
        ##if '__' not in attribute:
        #print(f"{attribute}")



async def main():
    i3 = await Connection(auto_reconnect=True).connect()
    workspaces = await i3.get_workspaces()

    i3.on(Event.WINDOW_FOCUS, on_window_focus)
    i3.on(Event.BINDING, binding_report)
    #i3.on(Event.WINDOW, on_window)
    #i3.on(Event.WORKSPACE_FOCUS, on_workspace_focus)

    # Reading from file
    #with open("./i3_info.cache", "r+") as cache_file:
        ## Reading form a file
        #print(cache_file.read())

    await i3.main()


# Proceed through the main() entrance.
if __name__ == "__main__":
    clear()
    asyncio.new_event_loop().run_until_complete(main())
