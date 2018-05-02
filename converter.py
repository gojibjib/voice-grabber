#!/usr/bin/env python3

import os, sys
from pydub import AudioSegment
from traceback import print_exc

if __name__ == "__main__":
    for root, dirs, files in os.walk('./files'):
        for f in files:
            if f.endswith('.mp3'):
                f_path = "{}/{}".format(root, f)
                new_file = f.strip(".mp3") + ".wav"
                new_file_path = "{}/{}".format(root, new_file)
                
                try:
                    song = AudioSegment.from_mp3(f_path)
                    song.export(new_file_path, format="wav")
                except:
                    print_exc()
                    sys.exit(1)
                
                try:
                    os.remove(f_path)
                except:
                    print_exc()
                    sys.exit(1)