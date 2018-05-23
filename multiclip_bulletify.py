"""

Extracts frames from all specified clips (synced). The timestamp to extract from is relative to the clip given a 00:00:00:00 timestamp.

usage: python3 multiclip_bulletify.py <alignment file> <output folder> <timestamp to extract frames>
This script expects all the video files to be in the SAME FOLDER as the alignment file!

"""

from sys import argv
from pathlib import Path
import os


FRAMES_PER_SECOND_INTEGER = 30
def parse_timestamp(timestamp_string):
	timestamp_data = timestamp_string.split(":")
	timestamp_pieces = []
	for item in timestamp_data:
		timestamp_pieces.append(int(item))
	
	return timestamp_pieces

if (len(argv) != 4):
	print("Incorrect number of paramaters. Expect multiclip_bulletify.py <alignment file> <output folder> <timestamp to extract frames>")
	exit(1)
script_name, clip_alignment_file_path, output_location, extraction_time_stamp = argv

clip_alignment_file = open(clip_alignment_file_path,'r')

clip_alignment_data = clip_alignment_file.read()

alignment_file_directory = "/".join(Path(clip_alignment_file_path).parts[:-1]) + "/"

clip_data = {}
for line in clip_alignment_data.split("\n"):
	split_data = line.split(" ")
	clip_data[split_data[0]] = split_data[1]


#Now use ffmpeg to extract the frames specified

extraction_time_stamp_parsed = parse_timestamp(extraction_time_stamp)

for file_name in clip_data:
	timestamp = parse_timestamp(clip_data[file_name])
	#Calculate our relative offsets
	hours = extraction_time_stamp_parsed[len(extraction_time_stamp_parsed) - 4] - timestamp[len(timestamp) - 4]
	minutes = extraction_time_stamp_parsed[len(extraction_time_stamp_parsed) - 3] - timestamp[len(timestamp) - 3]
	seconds = extraction_time_stamp_parsed[len(extraction_time_stamp_parsed) - 2] - timestamp[len(timestamp) - 2]
	frames = extraction_time_stamp_parsed[len(extraction_time_stamp_parsed) - 1] - timestamp[len(timestamp) - 1]
	
	#Keep all time values positive
	if (frames < 0):
		frames += FRAMES_PER_SECOND_INTEGER
		seconds -= 1;
		if (seconds < 0):
			seconds += 60
			minutes -= 1;
			if (minutes < 0):
				minutes += 60
				hours -= 1;
	
	#reduce everything to seconds as its our most accurate unit we can use in ffmpeg seek
	seek_seconds = (hours * 3600) + (minutes * 60) + seconds
	#video filter option
	video_filter_string = "-vf 'select=gte(n\\," + str(frames) + ")'"
	
	#command
	command_string = "ffmpeg -y -ss " + str(seek_seconds) + " -i " + alignment_file_directory + file_name + " -vf yadif -t 1 " + video_filter_string + " -f image2 " + output_location + "/" + file_name + ".JPG"
	os.system(command_string)
	print(command_string)



