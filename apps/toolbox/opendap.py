from pydap.client import open_url


def generate_url(date, level, version):
    opendap_url = []
    base_url = "https://podaac-opendap.jpl.nasa.gov/opendap/hyrax/allData/cygnss/"+level+"/"+version+"/"
    date_string = str(date.year) + str(date.month).zfill(2) + str(date.day).zfill(2)

    if version == "v2.1":
        v = "a21.d21"
    elif version == "v3.0":
        v = "a30.d31"

    if level == "L1":
        for satellite_number in range(8):
            specific_url = "/cyg0" + str(satellite_number+1) + ".ddmi.s" + date_string + "-000000-e" + date_string + "-235959.l1.power-brcs."+v+".nc"
            opendap_url.append(base_url + str(date.year) + "/" + str(date.timetuple().tm_yday).zfill(3) + specific_url)

    elif level == "L2":
        specific_url = "/cyg.ddmi.s" + date_string + "-000000-e" + date_string + "-235959.l2.wind-mss."+v+".nc"
        opendap_url.append(base_url + str(date.year) + "/" + str(date.timetuple().tm_yday).zfill(3) + specific_url)

    elif level == "L3":
        if version == "v2.1":
            v = "a10.d21"
        specific_url = "/cyg.ddmi.s" + date_string + "-003000-e" + date_string + "-233000.l3.grid-wind."+v+".nc"
        opendap_url.append(base_url + str(date.year) + "/" + str(date.timetuple().tm_yday).zfill(3) + specific_url)

    return opendap_url


def collect_dataset(url):
    try:
        dataset = open_url(url, output_grid=False)
    except:
        dataset = None
    return dataset


def clock_to_seconds(time):
    return sum(x * int(t) for x, t in zip([3600, 60, 1], str(time).split(":")))
