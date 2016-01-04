from util import *
from features import *

def main():
	a = 1;
	ictal_contents, interictal_contents, test_contents = load_for_patient('../clips/Patient_1')
	# import pdb; pdb.set_trace();

	getAllFeatures(ictal_contents)


if __name__ == '__main__':
	# raw_input("Press enter to begin")
	main()
	raw_input("Press enter to finish");