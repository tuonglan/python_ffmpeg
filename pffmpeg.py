import os, subprocess

import helper
import pffprobe as FFPROBE

FFMPEG_CMD = os.environ.get('FFMPEG_CMD', 'ffmpeg')


def extract_compressed_audio(in_file, start_ts, duration, out_file=None):
    # Get audio info
    audio_stream = FFPROBE.get_compressed_audio_stream(in_file)
    if 'aac' == audio_stream['codec_name']:
        audio_fmt = 'adts'
    elif 'ac3' == audio_stream['codec_name']:
        audio_fmt = 'ac3'
    else:
        audio_fmt = 'matroska'

    if out_file:
        cmd = [FFMPEG_CMD, '-i', in_file, '-map', "0:%s" % audio_stream['index'], '-c:a', 'copy',
               '-ss', helper.ts_to_timestr(start_ts), '-t', helper.ts_to_timestr(duration), out_file]
        try:
            result = subprocess.run(cmd, capture_output=True, check=True)       
        except subprocess.CalledProcessError as e:
            raise Exception("Can't execute command: %s\n%s\n" % (cmd, e.stderr.decode()))

        return None
    else:
        cmd = [FFMPEG_CMD, '-i', in_file, '-map', "0:%s" % audio_stream['index'], '-c:a', 'copy',
               '-ss', helper.ts_to_timestr(start_ts), '-t', helper.ts_to_timestr(duration), '-f', audio_fmt, '-']
        try:
            result = subprocess.run(cmd, capture_output=True, check=True)       
        except subprocess.CalledProcessError as e:
            raise Exception("Can't execute command: %s\n%s\n" % (cmd, e.stderr.decode()))
        return result.stdout


if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser()

    parser.add_argument('--action', type=str, choices=['test_extract_compressed_audio'], help='Choose function to test')
    parser.add_argument('--input', type=str, help='Input file')
    parser.add_argument('--output', type=str, default=None, help='Output file')
    parser.add_argument('--start_ts', type=int, help='Starting timestamp of the video')
    parser.add_argument('--duration', type=int, help='The duration of the captrue')

    args = parser.parse_args()

    if args.action == 'test_extract_compressed_audio':
        data = extract_compressed_audio(args.input, args.start_ts, args.duration)

        with open(args.output, 'wb') as sout:
            sout.write(data)

