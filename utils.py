import NDIlib as ndi
import time

def findNDIsources():
    if not ndi.initialize():
        return 0
    ndi_find = ndi.find_create_v2()
    if ndi_find is None:
        return 0
    t = time.time()

    while time.time() - t < 1.0 * 0.05:
        if not ndi.find_wait_for_sources(ndi_find, 100):
            # print('No change to the sources found.');
            continue
        sources = ndi.find_get_current_sources(ndi_find)
        #print('\n PGM Network sources (%s found).' % len(sources))

    return sources