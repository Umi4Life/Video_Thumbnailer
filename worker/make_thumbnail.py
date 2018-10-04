#!/usr/bin/env python3

from moviepy.editor import *
import sys

def makeGif(a, b):

	clip = VideoFileClip(a)
	clip = clip.resize((720,460))
	duration = clip.duration
	clip = clip.subclip(duration-((2.0/3)*duration))
	print(clip.duration)
	if(clip.duration>5):
		clip = clip.subclip(0,5)

	clip.write_gif(b, fps = 15)

# if __name__ == '__main__':
# 	inFile, outFile = sys.argv[1], sys.argv[2]
# 	makeGif(inFile,outFile)