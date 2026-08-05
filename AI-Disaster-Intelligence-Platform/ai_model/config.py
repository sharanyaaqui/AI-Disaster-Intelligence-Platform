IMAGE_SIZE = (224, 224)

BATCH_SIZE = 32

EPOCHS = 10

NUM_CLASSES = 4

CLASS_NAMES = [
    "cyclone",
    "earthquake",
    "flood",
    "wildfire"
]
NUM_CLASSES = len(CLASS_NAMES)
TRAIN_PATH = "ai_model/dataset/train"
TEST_PATH = "ai_model/dataset/test"
VALIDATION_PATH = "ai_model/dataset/validation"

MODEL_PATH = "ai_model/models/disaster_classifier.keras"

