import gzip
import pickle

# Load your model
with open('trained_multilingual_emotion_model.pkl', 'rb') as f:
    model = pickle.load(f)

# Compress and save the model
with gzip.open('trained_multilingual_emotion_model.pkl.gz', 'wb') as f:
    pickle.dump(model, f)