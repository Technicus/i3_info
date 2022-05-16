# i3_info
A tool to display information about i3 window manager.<br>
Inspired by bublabs top secret technology `i3_info`.<br>
Watch bublabs video explaination of the utility ["i3wm HOWTO scratchpad and start programs (i3run)"](https://www.youtube.com/watch?v=wKuQzx6jC_I&t=6m50s).<br>

## Bugs
The program will eventually fail due to a JSON parse error in the line: `tree = await i3.get_tree()`.

### Error
```
Traceback (most recent call last):
  File "/home/technicus/.config/i3/Macro_buttons/i3_info/development/./i3_info.py", line 135, in <module>
    asyncio.new_event_loop().run_until_complete(main())
  File "/usr/lib/python3.10/asyncio/base_events.py", line 646, in run_until_complete
    return future.result()
  File "/home/technicus/.config/i3/Macro_buttons/i3_info/development/./i3_info.py", line 129, in main
    await i3.main()
  File "/home/technicus/.local/lib/python3.10/site-packages/i3ipc/aio/connection.py", line 664, in main
    await self._main_future
  File "/home/technicus/.local/lib/python3.10/site-packages/i3ipc/aio/connection.py", line 34, in handler_coroutine
    await handler(conn, data)
  File "/home/technicus/.config/i3/Macro_buttons/i3_info/development/./i3_info.py", line 36, in on_window_focus
    tree = await i3.get_tree()
  File "/home/technicus/.local/lib/python3.10/site-packages/i3ipc/aio/connection.py", line 589, in get_tree
    return Con(json.loads(data), None, self)
  File "/usr/lib/python3.10/json/__init__.py", line 346, in loads
    return _default_decoder.decode(s)
  File "/usr/lib/python3.10/json/decoder.py", line 337, in decode
    obj, end = self.raw_decode(s, idx=_w(s, 0).end())
  File "/usr/lib/python3.10/json/decoder.py", line 353, in raw_decode
    obj, end = self.scan_once(s, idx)
json.decoder.JSONDecodeError: Unterminated string starting at: line 1 column 36441 (char 36440)

```
