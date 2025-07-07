import pystk

pystk.init(pystk.GraphicsConfig.hd())

config = pystk.RaceConfig(track='lighthouse', num_kart=1)
race = pystk.Race(config)
race.start()

import time
time.sleep(5)  # Laisse le temps à la fenêtre de s'afficher

race.stop()
del race
pystk.clean()