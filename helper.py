def ts_ms_to_timestr(ts_ms):
    millisecs = ts_ms % 1000
    all_secs = int(ts_ms / 1000)

    secs = all_secs % 60
    mins = int(all_secs/60) % 60
    hours = int(all_secs/3600)

    return "%02d:%02d:%02d,%03d" % (hours, mins, secs, millisecs)


def ts_to_timestr(ts):
    ts = int(ts)
    secs = ts % 60
    mins = int(ts/60) % 60
    hours = int(ts/3600)

    return "%02d:%02d:%02d" % (hours, mins, secs)
