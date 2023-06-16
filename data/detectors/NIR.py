pixelScale = 0.015
ccdSize = (4096, 4096)
bias = 100
# This is the total system gain, same as in camera.yaml.
# In the real data, the pixel values have had an initial gain from the ASIC
# applied, which is recorded in the W_H4GAIN header keyword (typically around
# 2.8), and this gain is removed from the system gain on read.
# In the simulator, we set W_H4GAIN=1. This avoids having to change the pixel
# values, but should have the correct effect.
gain = 9.0
readNoise = 20.0
interCcdGap = 0.0
