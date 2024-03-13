import os, subprocess

import json

FFPROBE_CMD = os.environ.get('FFPROBE_CMD', 'ffprobe')


def get_info(in_file, out_file=None):
    cmd = [FFPROBE_CMD, '-v', 'quiet', '-print_format', 'json', '-show_streams', '-show_format', in_file]

    result = subprocess.run(cmd, capture_output=True, check=True)
    
    if out_file:
        with open(out_file, 'w') as sout:
            sout.write(result.stdout.decode())

    s = result.stdout.decode()
    return json.loads(s)

def get_audio_language(stream):
    lang = stream.get('tags', {}).get('language')
    if lang == 'en' or lang == 'eng' or lang == 'English' or lang == 'english':
        lang = 'English'
    if lang == 'vi' or lang == 'vie' or lang == 'Vietnamese' or lang == 'vietnamese':
        lang = 'Vietnamese'

    return lang


# Audio priority
# 1 : aac, 2 : ac3, 3 : <others>
def get_compressed_audio_stream(in_file):
    def _get_codec_priority(codec):
        if 'aac' == codec:
            return 1
        elif 'ac3' == codec:
            return 2
        else:
            return 3

    info = get_info(in_file)

    audio_stream = None
    for stream in info['streams']:
        if 'audio' == stream['codec_type']:
            if None == audio_stream:
                audio_stream = stream
            else:
                current_codec_prio = _get_codec_priority(audio_stream['codec_name'])
                new_codec_prio = _get_codec_priority(stream['codec_name'])
                current_lang = get_audio_language(audio_stream)
                new_lang = get_audio_langauge(stream)

                if 'English' == current_lang:
                    if 'English' == new_lang and current_codec_prio < new_codec_prio:
                        audio_stream = stream
                elif 'English' == new_lang:
                    audio_stream = stream
                elif current_codec_prio < new_codec_prio:
                    audio_stream = stream

    return audio_stream


if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser()

    parser.add_argument('--action', type=str, choices=['test_get_info'], help='Choose function to test')
    parser.add_argument('--input', type=str, help='Input file')
    parser.add_argument('--output', type=str, default=None, help='Output file')

    args = parser.parse_args()

    if args.action == 'test_get_info':
        info = get_info(args.input, args.output)
        print(info)

