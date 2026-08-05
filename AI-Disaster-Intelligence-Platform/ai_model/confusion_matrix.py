import numpy as np
import matplotlib.pyplot as plt

from sklearn.metrics import confusion_matrix
from sklearn.metrics import ConfusionMatrixDisplay
from sklearn.metrics import classification_report

from preprocessing import test_data
from model import model

# Predict on test dataset
predictions = model.predict(test_data)

predicted_classes = np.argmax(predictions, axis=1)

true_classes = test_data.classes

class_names = list(test_data.class_indices.keys())

# Confusion Matrix
cm = confusion_matrix(true_classes, predicted_classes)

disp = ConfusionMatrixDisplay(
    confusion_matrix=cm,
    display_labels=class_names
)

disp.plot(cmap="Blues")

plt.title("Confusion Matrix")

plt.savefig("ai_model/evaluation/confusion_matrix.png")

plt.show()

# Classification Report
report = classification_report(
    true_classes,
    predicted_classes,
    target_names=class_names
)

print(report)

with open("ai_model/evaluation/classification_report.txt","w") as f:
    f.write(report)

print("Classification Report Saved!")