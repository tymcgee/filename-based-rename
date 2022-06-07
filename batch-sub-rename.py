# Tynan McGee
# 5/2022
# Original command line version, made for renaming subtitle/audio files to
# match a video file name

import os

def pad(n):
    """ turn an int n into a string with a padded 0 if n is one digit """
    if n < 10:
        return '0' + str(n)
    return str(n)

folder = input('Full path to folder containing videos and subtitles:\n')
folder = os.path.abspath(folder)
folder = os.path.join(folder, "")  # Add the trailing slash
audio_ext = '.opus'
sub_ext = '.srt'
recursing = input('Recurse into subdirectories? (1) yes (2) no  ') == "1"
use_audio = input('Rename audio files? (1) yes (2) no  ') == "1"
use_subs = input('Rename subtitles? (1) yes (2) no  ') == "1"
if use_audio:
    audio_ext = input('What is the audio extension? (.mp3, .opus, etc)  ')
    num_of_audio = int(input('How many audio files should be renamed per video?  '))
    audio_suffixes = []
    for i in range(num_of_audio):
        audio_suffixes.append(input(f'Write the suffix for the audio file #{i+1}  '))
if use_subs:
    sub_ext = input('What is the subtitle extension? (.srt, .ass, etc)  ')
    num_of_subs = int(input('How many subtitle files should be renamed per video?  '))
    sub_suffixes = []
    for i in range(num_of_subs):
        sub_suffixes.append(input(f'Write the suffix for subtitle #{i+1}  '))
vid_ext = input('What is the video extension? (.mkv, .mp4, etc)  ')


vid_list = []
sub_list = []
audio_list = []
sub_sources = []
sub_dests = []
audio_sources = []
audio_dests = []

if recursing:
    for root, dirs, files in os.walk(folder):
        for filename in files:
            if filename.endswith(vid_ext):
                vid_list.append(os.path.join(root, filename))
            elif filename.endswith(sub_ext):
                sub_list.append(os.path.join(root, filename))
            elif filename.endswith(audio_ext):
                audio_list.append(os.path.join(root, filename))
else:
    for i in os.listdir(folder):
        if i.endswith(vid_ext):
            vid_list.append(i)
        elif i.endswith(sub_ext):
            sub_list.append(i)
        elif i.endswith(audio_ext):
            audio_list.append(i)
sub_list.sort()
vid_list.sort()
audio_list.sort()

for i in range(len(vid_list)):
    vid = vid_list[i]
    base_name = vid[:-4]
    if use_subs:
        # Remove .mkv from end of vid name and add suffix.srt
        for sub_num in range(num_of_subs):
            sub = sub_list[num_of_subs*i + sub_num]
            new_sub_name = base_name + '_' + sub_suffixes[sub_num] + sub_ext
            sub_source = os.path.join(folder, sub)
            sub_dest = os.path.join(folder, new_sub_name)
            sub_sources.append(sub_source)
            sub_dests.append(sub_dest)
            print(sub_source, '-->', sub_dest)
    if use_audio:
        for audio_num in range(num_of_audio):
            audio = audio_list[num_of_audio*i + audio_num]
            new_audio_name = base_name + '_' + audio_suffixes[audio_num] + audio_ext
            audio_source = os.path.join(folder, audio)
            audio_dest = os.path.join(folder, new_audio_name)
            audio_sources.append(audio_source)
            audio_dests.append(audio_dest)
            print(audio_source, '-->', audio_dest)

if input('\nDoes this look okay? [y/N] ') in ('Y', 'y'):
    if use_subs:
        print('Renaming subtitles...')
        for src, dst in zip(sub_sources, sub_dests):
            os.rename(src, dst)
        print('Subtitles renamed.')
    if use_audio:
        print('Renaming audio files...')
        for src, dst in zip(audio_sources, audio_dests):
            os.rename(src, dst)
        print('Audio files renamed.')
else:
    print('Aborting..')
    input()