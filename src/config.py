# Absolute Screen Dimensions
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

# Relative coordinate landmarks
CTR_X = SCREEN_WIDTH / 2
CTR_Y = SCREEN_HEIGHT / 2

# Distance boundary sides are from the center of the screen
X_RATIO = 5
Y_RATIO = 6
RATIO_SCALE = min(SCREEN_HEIGHT / 18, SCREEN_WIDTH / 32)
X_PADDING = X_RATIO * RATIO_SCALE
Y_PADDING = Y_RATIO * RATIO_SCALE

# Coordinates of the game boundary
LEFT = CTR_X - X_PADDING
TOP = CTR_Y + Y_PADDING
BOTTOM = CTR_Y - Y_PADDING
RIGHT = CTR_X + X_PADDING