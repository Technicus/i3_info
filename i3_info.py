#!/bin/python



import json
from os import system
from i3ipc.aio import Connection
from i3ipc import Event
import asyncio


def clear():
    system("clear")


# Define a callback to be called when you switch workspaces.
def on_workspace_focus(i3, event):
    # The first parameter is the connection to the ipc and the second is an object
    # with the data of the event sent from i3.
    if event.current:
        print('on_workspace_focus(i3, event):')
        for window in event.current.leaves():
            print(f"event:\n  {window.name}")
            print(f"event:\n  {event}\n")



def on_window(i3, event):
    print(f"on_window():\n  {event}\n")


# Report event and tree information
async def on_window_focus(i3, event):
    i3_tree = await i3.get_tree()
    # Capture event data.
    i3_ipc_event_data = event.ipc_data
    # Convert into JSON:
    i3_ipc_event_data_formatted = json.dumps(i3_ipc_event_data, indent=4)
    with open("./i3_info.cache", "w") as cache_file:
    # Writing data to a file
        cache_file.write(f"event:\n  {event}\n\n")
        cache_file.write(f"i3.get_tree():\n  {i3_tree}\n\n")
        cache_file.write(f"event.ipc_data():\n  {i3_ipc_event_data_formatted}\n")


async def main():
    i3 = await Connection(auto_reconnect=True).connect()
    workspaces = await i3.get_workspaces()

    i3.on(Event.WINDOW, on_window)
    i3.on(Event.WINDOW_FOCUS, on_window_focus)
    i3.on(Event.WORKSPACE_FOCUS, on_workspace_focus)

    # Reading from file
    #with open("./i3_info.cache", "r+") as cache_file:
        ## Reading form a file
        #print(cache_file.read())

    await i3.main()


# Proceed through the main() entrance.
if __name__ == "__main__":
    clear()
    asyncio.new_event_loop().run_until_complete(main())
