#!/usr/bin/env python3
from __future__ import print_function
import urllib.request
import shutil
import subprocess
import decode
import argparse


def convert_audio_file(infile, outfile):
    args = ['ffmpeg', '-i', infile, outfile]
    subprocess.run(args, check=True)


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('-url')
    parser.add_argument('-o', '--output-wave', default='song.wav')
    args = parser.parse_args()

    url = args.url
    out_filename = args.output_wave
    filename = 'song.mp3'

    # Download the file from `url` and save it locally under `filename`:
    with urllib.request.urlopen(url) as response, open(filename, 'wb') as outfile:
        # copy from HTTP response file-like object to a file
        print('Downloading from {}'.format(url))
        shutil.copyfileobj(response, outfile)

    print('Saved to a file.')
    print('Reading audio from mp3, doing audio processing and saving to wav...')
    decode.decode(filename, out_filename)

    print('Saved!')


if __name__ == '__main__':
    main()

