Prof. B.L. Bardakjian   berj@cbl.utoronto.ca 
Title:  Home monitoring of epileptic patients
Students: Akshaya Pragadeeshram, Richa Rajgolikar, Divya Dadlani, Rahul Verma
This project deals with developing software parts of a headset system for monitoring of  brain states from the EEG of epileptic patients. This involves signal processing of the EEG signals to determine feature sets to be used in a machine learning environment to classify the brain states and their transitions to seizure states. These decisions will be provided to a  wireless transmission system to a "smart" phone/receiver. The data used was sourced from the Seizure Detection Challenge on Kaggle (www.kaggle.com/c/seizure-detection)


Using Python 2.7 on the ECF machines:

scl enable python27 $SHELL

Check Python version

python --version

Install a missing module:
Make sure you're running Python 2.7 before doing this step

pip install --user <module-name>

Dependencies: 
* Python 2.7
* Numpy
* SciPy
* Pybrain
* Pickle

Files:
* nn.py - set up of the neural net
* run_model.py - set up of training, validation and test sets and results
* request.py - script to send a signal to the mobile application via Google push notifications
* final_net/ - our final neural net implementation, results and test set
* webapp/ - files to demonstrate the neural net as an interactive webapp
* other_code/ - other code that we wrote but did not use for the end product

The data sets were saved and retrieved using Pickle. The neural net was saved using PyBrain's built in functions.
