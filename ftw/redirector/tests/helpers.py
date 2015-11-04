
def make_rules(*redirects):
    return [{'source_path': src,
             'destination_path': dst}
            for (src, dst) in redirects]
