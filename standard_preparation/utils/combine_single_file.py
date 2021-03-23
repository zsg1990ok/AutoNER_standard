import os

def combine_lines(old_path):
	rline = ""
	with open(old_path, "r") as old_file:
		for line in old_file:
			rline += line.replace('\n','\t')
	return rline

if __name__ == '__main__':
	original_path = "../../data/original_standard_files/"
	converted_path = "../../data/converted_standard_files/"
	for file in os.listdir(original_path):
		old_path = os.path.join(original_path, file)
		new_path = os.path.join(converted_path, file)
		with open(new_path, "w") as new_file:
			line = combine_lines(old_path)
			new_file.write(line+'\n')