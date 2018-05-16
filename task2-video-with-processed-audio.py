#!/usr/bin/env python3
from __future__ import print_function
import urllib.request
import shutil
import subprocess
import decode
import argparse


def embed_audio_to_video(audio_file, video_file, audio_encoding, output_file, overwrite='-y'):
    """
        Here we can use WAV with AVI or AAC with MP4.
        MP4 cannot hold WAV audio.
    """
    args = ['ffmpeg', overwrite, '-i', audio_file, '-i', video_file,
            '-acodec', audio_encoding, '-vcodec', 'copy', # Keep original video
            '-map', '0:a:0', '-map', '1:v:0', # discard any audio from the original mp4 video, use only the `audio_file`
            '-shortest' # give output file length of shortest input (audio/video)
           ]

    if audio_encoding == 'aac':
        args.extend(['-strict', 'experimental']) # enable experimental aac

    args.extend([output_file])

    subprocess.run(args, check=True)
    # ffmpeg -i processed.wav -i video_with_processed_sound.mp4 -acodec aac -map 1:v:0 -map 0:a:0 -vcodec copy -strict experimental merged_aac.mp4


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('-url-video')
    parser.add_argument('-url-audio')
    parser.add_argument('--audio-codec', default='copy') # if no codec specified, use original audio (WAV)
    parser.add_argument('-o', '--output-mp4', default='video-with-processed-audio.mp4')
    args = parser.parse_args()

    url_video = args.url_video
    url_audio = args.url_audio
    out_mp4_filename = args.output_mp4
    audio_codec = args.audio_codec
    tmp_video = 'tmp.mp4'
    tmp_audio = 'song.mp3'
    processed_audio = 'song.wav'

    # Download the video from url and save it locally under video_filename:
    with urllib.request.urlopen(url_video) as response, open(tmp_video, 'wb') as outfile:
        # copy from HTTP response file-like object to a file
        print('Downloading video from {}'.format(url_video))
        shutil.copyfileobj(response, outfile)

    # Download the file from `url` and save it locally under `filename`:
    with urllib.request.urlopen(url_audio) as response, open(tmp_audio, 'wb') as outfile:
        # copy from HTTP response file-like object to a file
        print('Downloading audio from {}'.format(url_audio))
        shutil.copyfileobj(response, outfile)

    print('Reading audio from mp3, doing audio processing and saving to wav...')
    decode.decode(tmp_audio, processed_audio)

    # Encode to lossless audio and embed to video
    embed_audio_to_video(processed_audio, tmp_video, audio_codec, out_mp4_filename)

    print('mp4 video with modified audio saved!')


if __name__ == '__main__':
    main()

