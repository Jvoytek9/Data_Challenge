# What is this
This was the initial prototype of the Kassandra Dashboard, and iteration 3/3 of the portable dashboard I had been working on since the surfactant dashboard.

# Installation
If interested in running a local version, clone this repo and make sure to have pip installed.

Then, make a separate virtualenv like so (this example makes a virtual environment named venv at the given path): python -m venv c:\path\to\myenv

copy the contents of the cloned repo into this new venv folder. Activate the venv like so: cd venv\path\to\myenv\Scripts then type "activate" and hit enter

The name of your venv should appear next to the command prompt. Now type: cd ..

And finally: pip install requirements.txt

Then, running the app/app.py file in your editor of choice will boot up a local Flask server, which you can then do as you please with.
