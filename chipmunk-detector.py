import argparse 
import sys
import os
import parselmouth
import numpy as np
from scipy.stats.mstats import gmean

def gmean_pitch_cal(wavpath):
    snd = parselmouth.Sound(wavpath)
    pitch = snd.to_pitch()
    pitch = pitch.selected_array['frequency']
    pitch = np.delete(pitch, np.where(pitch == 0))
    return gmean(pitch)

def wav_parser(wavefile_path):
    wav = dict()
    for f in os.listdir(wavefile_path):
        wav_id = f.split('.')[0]
        wav[wav_id] = wavefile_path + f
    return wav

if __name__ == '__main__':
    
    args = sys.argv[1:]
    parser = argparse.ArgumentParser(description= "Parses command.")
    
    parser.add_argument("-w", "--wavefiles", help="wave files path.")
    parser.add_argument("-o", "--output", help="destination output file.")
    parser.add_argument("-r", "--ratio", help="detection ratio.", default=300)
    
    options = parser.parse_args(args)

    wavefile_path = options.wavefiles
    out_path = options.output
    ratio = options.ratio

    wav = wav_parser(wavefile_path)    

    with open(out_path, 'w') as outfile:
        for wav_id in sorted(list(wav.keys())):
            gmean_pitch = gmean_pitch_cal(wav[wav_id])
            if gmean_pitch < ratio :
                print("{}".format(wav[wav_id]), file=outfile)
                print("{}".format(wav[wav_id]))
            else:
                print("{} is chipmunk (not included in output file".format(wav_id))