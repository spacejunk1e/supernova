# Configuration settings and constants
BASE_POST_POINT = 1
REACTION_POINTS = {
    'heart': 2,
    'wow': 3,
    'laugh': 1,
    'generic': 0.5,  # Any reaction that isn't explicitly scored
    'super': 5  # Any super reaction, regardless of type
}
DIVERSITY_MULTIPLIER = 1.2
FREQUENCY_DECAY_THRESHOLD = 5
FREQUENCY_DECAY_RATE = 0.5
UNIQUE_REACTOR_BONUS = 0.5
CONSISTENCY_BONUS = 10
CURATOR_BONUS = 15
