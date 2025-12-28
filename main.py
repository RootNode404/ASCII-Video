import cv2
import numpy as np
import sys

# Change these to your likeing
chars = "!@#$%^&*(_+)}|[]\\:\";'<{>?,./"  # Characters to use.
res = 200  # Change this for the resolution, higher numbers = lower fps/more delay

ASCII = np.array(list(chars))

# Capture the camera
# If you get a "can't open camera by index" error try changing this varible to another one digit numbner
cam_index = 0
cam = cv2.VideoCapture(cam_index, cv2.CAP_V4L2)

# Main loop
while True:

    # Get a fram from the camera
    ret, frame = cam.read()

    # Get height and width
    h, w, _ = frame.shape
    rows = int(res * h / w * 0.5)


    small = cv2.resize(frame, (res, rows))
    color = cv2.cvtColor(small, cv2.COLOR_BGR2GRAY)

    idx = (color / 256 * len(ASCII)).astype(np.int32)
    chars = ASCII[idx]

    # Compile lines with color
    out_lines = []
    for y in range(rows):
        line = []
        for x in range(res):
            b, g, r = small[y, x]
            c = chars[y, x]
            line.append(f"\x1b[38;2;{r};{g};{b}m{c}")
        out_lines.append("".join(line))

    # Print final ascii frame to terminal
    sys.stdout.write("\n".join(out_lines))
    sys.stdout.flush()

