def parse_duration(s):
    if s.isdigit():
        return int(s)
    d, u = s[:-1], s[-1]
    if not d.isdigit():
        raise ValueError
    if u == 's':
        return int(d)
    if u == 'm':
        return int(d) * 60
    if u == 'h':
        return int(d) * 60 * 60
    if u == 'd':
        return int(d) * 60 * 60 * 24
    raise ValueError
