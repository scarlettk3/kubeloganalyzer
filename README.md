KUBELOGANALYZER
----------------
it is web application used to upload error log files and get analysis by Mistral AI

how to run:
1. create a virtual environment
python -m venv venv
venv/Scripts/activate
2. install necessary packages
pip install flask requests
3. in the app.py keep your Mistral AI API, no need of changing the Mistral Url.
4. run the application:
python app.py

it will start and redirect you to the web application(localhost)
Now you can upload the log files and can get the analysis

you can change the "prompt" in the app.py to get the kind of analysis you need.
