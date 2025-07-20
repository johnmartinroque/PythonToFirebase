1. Install dependencies:
   pip install -r requirements.txt

2. Collect gesture data:
   py collection_data.py

   👉 Press:
      - '1' to save as gesture1
      - '2' to save as gesture2
      - '3' to save as gesture3
      - 'q' to quit

3. Train the model:
   py train_model.py

4. Run the gesture recognition system:
   py camera.py




##############################################
 Firebase Setup (For camera.py & speech.py)

Make sure to replace this line in both files:

   cred = credentials.Certificate("credentials.json")
   firebase_admin.initialize_app(cred, {
       'databaseURL': 'https://pyfire-da0f6-default-rtdb.firebaseio.com/'
   })

👉 Replace `'credentials.json'` 

##############################################
