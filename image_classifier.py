from tensorflow.keras.models import load_model
from tensorflow.keras.utils import image_dataset_from_directory, load_img, img_to_array
import numpy as np


model = load_model("C:/Users/Home/Downloads/HullProj.keras")
names = ['Tuberculosis', 'NORMAL', 'PNEUMONIA']



def image_prediction(image_path : str) -> str:
	"""Classifies an uploaded image from a given file path."""
	image = img_to_array(load_img(image_path, target_size=(224, 224)))/255.0
	image = np.expand_dims(image, 0)

	prediction = model.predict([image])

	return names[np.argmax(prediction)]











