# Multiclip Bullet Time / Time Slice Frame Generator

![demo](demo.gif)

This is a short script for extracting frames from multiple cameras according to a synchronization profile. This script was used to create the demo seen above. I created this short program because it is *very* tedious manually exporting frames from nine different cameras (let alone the suggested 40+!) in Final Cut.

###Requirements

1. python3
2. ffmpeg

###Usage

1 . Create a folder which holds all the camera shots for the scene

2 . Create a sync profile. You can call this what ever you want but you must place it in the same folder as your clips. This file contains the offsets of each file, one per line. For example:

```
1.MP4 00:00:00:00
2.MP4 00:00:01:12
4.MP4 00:00:03:20 
```

The timestamps are in the following format: (HOURS):(MINUTES):(SECONDS):(FRAME). This sync file essentially tells the script how to offset each clip in order to make their frames perfectly line up. For example, the definition above tells the program that '2.MP4' picks up one second and twelve frames after 1.MP4. You can, in theory, have no clips starting at 00:00:00:00 however that's an undefined behavior.  

3 . Execute the script as `python3 multiclip_bulletify.py <alignment file> <output folder for extracted frames> <timestamp to extract frames>`