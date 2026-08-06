# AI Integration Guide

## Import

```python
from ai_model.predict import predict_disaster
```

## Predict

```python
result = predict_disaster(image_path)
```

## Output

```json
{
    "prediction":"Flood",
    "confidence":99.1,
    "risk":"High",
    "actions":[]
}
```

The backend should send the uploaded image path to
predict_disaster() and return the resulting dictionary
as JSON.