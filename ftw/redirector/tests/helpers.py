
def make_rules(*redirects):
    return [{'source_path': src,
             'destination': dst}
            for (src, dst) in redirects]
