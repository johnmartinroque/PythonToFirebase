Steps:
pip install -r requirements.txt
py collecton_data.py
py train.py
py camera.py

Need to be replaced
Speech.py
cred = credentials.Certificate("credentials.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://pyfire-da0f6-default-rtdb.firebaseio.com/'  # Replace with your Firebase URL
})

camera.py
cred = credentials.Certificate("credentials.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://pyfire-da0f6-default-rtdb.firebaseio.com/'
})



