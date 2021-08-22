def session_cache_path(session, caches_folder):
    return caches_folder + session.get('uuid')

def convert_time(milliseconds):
    ms = int(milliseconds)
    s = (ms/1000) % 60
    min = (ms / (1000*60)) % 60
    return ("%d:%02d" % (min, s))

def get_artists(a_list):
    artists = ""
    for a in a_list:
        artists += f"{a['name']}, "
    return artists[:-2]
