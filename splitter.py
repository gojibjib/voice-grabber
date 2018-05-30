#!/usr/bin/env python3

import os, sys
from pydub import AudioSegment
from traceback import print_exc

if __name__ == "__main__":
    for root, dirs, files in os.walk('./files'):
        for f in files:
            if f.endswith('.wav'):
                test = 0
                f_path = "{}/{}".format(root, f)
                try:
                    sound = AudioSegment.from_wav(f_path)
                    #groesser als 20 sek
                    if(len(sound)>20000):
                        # slice into 10s frames
                        slices = sound[::10000]
                        counter=1
                        for element in slices:
                            #falls groesser als 3 sekunden
                            if(len(element)>3000):
                                name, ext = os.path.splitext(f)
                                new_name = "{}_{}.wav".format(name, counter)
                                save_path = os.path.join(root, new_name)
                                element.export(save_path, format="wav")
                                #print("Exporting: {}".format(new_name))
                                counter+=1
                        
                        # If file gets sliced, delete old one
                        try:
                            os.remove(f_path)
                        except:
                            print_exc()
                            sys.exit(1)

                except:
                    print_exc()
                    sys.exit(1)
                

                if test == 10:
                    sys.exit(0)