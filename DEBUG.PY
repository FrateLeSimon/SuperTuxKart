from pydualsense import *

ds = pydualsense()
ds.init()
print("DualSense connecté")
ds.setLightBarColor(255, 0, 0)  # LED rouge
ds.close()
