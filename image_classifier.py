from tensorflow.keras.models import load_model
from tensorflow.keras.utils import image_dataset_from_directory, load_img, img_to_array
import numpy as np



image_path = 'C:/Users/Home/OneDrive/Desktop/Tuberculosis/Tuberculosis-2.png'
def image_prediction(image_path):
	model = load_model("C:/Users/Home/Downloads/TBvsPneuProj.keras")
	names = ['Tuberculosis', 'NORMAL', 'PNEUMONIA']
	image = img_to_array(load_img(image_path, target_size=(256, 256)))
	image = np.expand_dims(image, 0)

	prediction = model.predict([image])

	return (names[np.argmax(prediction)])

pred = image_prediction(image_path)
print(pred)# Tuberculosis







