import pickle
import matplotlib.pyplot as plt
import os

# Create evaluation folder
os.makedirs("ai_model/evaluation", exist_ok=True)

# Load history
with open("ai_model/history.pkl", "rb") as f:
    history = pickle.load(f)

# ---------------- Accuracy Graph ---------------- #

plt.figure(figsize=(8,5))

plt.plot(history["accuracy"], label="Training Accuracy")
plt.plot(history["val_accuracy"], label="Validation Accuracy")

plt.title("Model Accuracy")
plt.xlabel("Epoch")
plt.ylabel("Accuracy")
plt.legend()
plt.grid(True)

plt.savefig("ai_model/evaluation/accuracy_graph.png")
plt.close()

# ---------------- Loss Graph ---------------- #

plt.figure(figsize=(8,5))

plt.plot(history["loss"], label="Training Loss")
plt.plot(history["val_loss"], label="Validation Loss")

plt.title("Model Loss")
plt.xlabel("Epoch")
plt.ylabel("Loss")
plt.legend()
plt.grid(True)

plt.savefig("ai_model/evaluation/loss_graph.png")
plt.close()

print("✅ Accuracy graph saved.")
print("✅ Loss graph saved.")
print("✅ Evaluation completed successfully.")