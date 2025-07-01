Steps:
1. pip install -r requirements.txt
2. py collecton_data.py
3. py train.py
4. py camera.py
##########################################
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



