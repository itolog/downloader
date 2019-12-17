#!/bin/bash
import subprocess
import os

import pafy
import ffmpeg

#
audio_path = os.fspath('C:/Users/itolog/Pictures/a-a.mp3')
video_path = os.path.normcase(r'C:/Users/itolog/Pictures/a.mp4')
final_path = os.path.normcase(r'C:/Users/itolog/Pictures/final.mp4')

video = pafy.new('https://www.youtube.com/watch?v=m5Y8UOKVCrI')
video_stream = video.videostreams
audio_stream = video.audiostreams
audio_download = audio_stream[1].download(filepath=audio_path)

download = video_stream[1].download(filepath=video_path)
# input_video = ffmpeg.input('a.mp4')
# added_audio = ffmpeg.input('a-a.mp4')
# #
# ffmpeg.concat(input_video, added_audio).output('out.mp4').run()
subprocess.run(f'ffmpeg -i {audio_path} -i {video_path} {final_path}', shell=True)

os.remove(audio_path)
os.remove(video_path)
