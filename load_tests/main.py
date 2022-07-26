import random
import time
from os import listdir
from os.path import isfile, join
from pathlib import Path

import molotov


PROJECT_ROOT = Path(__file__).absolute().parent.parent
ASSETS_DIR = PROJECT_ROOT / "assets"
_RPS = {}


def _now():
    return int(time.time())


@molotov.scenario(weight=100)
async def _test(session):
    images = [str(ASSETS_DIR / f) for f in listdir(str(ASSETS_DIR)) if isfile(join(str(ASSETS_DIR), f))]
    random_image_path = random.choice(images)

    files = {'image': open(random_image_path, 'rb')}

    async with session.post('http://127.0.0.1:8080/', data=files, timeout=1) as resp:
        assert resp.status == 200


@molotov.events()
async def record_time(event, **info):
    if event == "sending_request":
        ts = _now()
        if ts in _RPS:
            _RPS[ts] += 1
        else:
            _RPS[ts] = 1


@molotov.global_teardown()
def display_average():
    print(f"\nMax RPS: {max(_RPS.values())}")
