from dotenv import load_dotenv
import os
from PIL import Image
import google.generativeai as genai
#from image_classifier import image_prediction
from google.api_core import retry
from databasetools import database_enginee, get_tables, table_discription, execute_query
import streamlit as st





load_dotenv()
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)

db_tools = [get_tables, table_discription, execute_query]




instruction = """
You are a helpful medical chatbox acting as a clinical decision support system (CDSS). Your role is to assist medical personnel by providing medical advice based on patient information.

You have access to the following tools to help guide your conversation:
- db_tools: a set of functions that interact with the ERP_proj database. This includes:
  - list_tables: Lists the tables in the database.
  - describe_table: Provides the schema of the database.
  - execute_query: Executes SQL queries on the database.

The information from these tools may not be available immediately, but you should engage in continuous conversation using the tools and schema as templates, do not enforce this. If you need more information, prompt the user to provide it. However, avoid repeatedly asking for the same information.

In this case, we have the following tables and columns in the database:
- **Vitals Table:**
  - Columns: ['vitals_id', 'Blood_pressure', 'Heart_rate', 'Respiratory_rate', 'Oxygen_saturation', 'Temperature', 'patient_id']
  - Purpose: Stores the vital signs for patients.

- **History Table:**
  - Columns: ['patient_id', 'name', 'history'], the patient ID, name and some information are in the history
  - Purpose: Stores patient history information, including diagnoses or symptoms presented.
-# **Querying Rules using foreign keys betwee vitals and history table **
- When retrieving a patient’s vitals, **automatically join the `Vitals` and `History` tables** using `patient_id`.
- Example SQL Query:
  ```sql
  SELECT h.name, h.history, v.Blood_pressure, v.Heart_rate, v.Respiratory_rate, v.Oxygen_saturation, v.Temperature
  FROM history h
  JOIN vitals v ON h.patient_id = v.patient_id
  WHERE h.name = 'John Jones';
-** Discharge Summary**
	if you are prompted to give a discharge summary, you should give a 200 word count of the signicant discussion - use the history and vitals databases to give a comprehensive summary
-Image like CXR result can be provided to you as well, you can use this to aid your discussion and diagnosis 

Your purpose is to ask relevant questions to reach a potential diagnosis and suggest medical treatment as the final output. Please ensure you maintain a conversational approach throughout the interaction.

If you are to provide a disclaimer about not being a medical expert, do so after the conversation. Make it clear that you are a clinical decision support system and not a medical professional.

Important notes:
- Always verify the details of the patient's condition before suggesting a diagnosis.
- If you're unsure about the diagnosis, ask follow-up questions.
- Engage the user with questions and use the database tools to gather the necessary information.
"""



model = genai.GenerativeModel(
    "models/gemini-1.5-flash-latest", tools=db_tools, system_instruction=instruction
)

retry_policy = {"retry": retry.Retry(predicate=retry.if_transient_error)}

chat = model.start_chat(enable_automatic_function_calling=True)


st.set_page_config(layout="wide")

col1, col2 = st.columns([2, 3])  # Adjust ratio as needed

with col2:
	st.title("Interactive Clinical Decision support System ")


	if "messages" not in st.session_state:
		st.session_state.chat = model.start_chat(enable_automatic_function_calling=True)
		st.session_state.messages = [{"role": "bot", "content": "Hi, how can I help?"}]


	for msg in st.session_state.messages:
		with st.chat_message(msg["role"]):
			st.write(msg["content"])


	if user_input := st.chat_input("Type your message..."):
	    # Display user message
	    st.session_state.messages.append({"role": "user", "content": user_input})

	    with st.chat_message("user"):
	        st.write(user_input)

	    response = st.session_state.chat.send_message(user_input)
	    bot_reply = response.text
	    st.session_state.messages.append({"role": "box", "content": bot_reply})

	    with st.chat_message("bot"):
	        st.write(bot_reply)




with col1:
    st.header("📊 Patient Vitals & CXR")
    
    # Example: Display vitals
    vitals = {
        "Blood Pressure": "90/50 mmHg",
        "Heart Rate": "105 bpm",
        "Respiratory Rate": "24 breaths/min",
        "Oxygen Saturation": "90%",
        "Temperature": "38°C"
    }
    st.table(vitals)

    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
	    image = Image.open(uploaded_file)
	    
	    # Display the image in the Streamlit app
	    st.image(image, caption="Uploaded Image", use_container_width =True)



