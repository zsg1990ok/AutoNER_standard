import os

def combine_lines(old_path):
	rline = ""
	with open(old_path, "r") as old_file:
		for line in old_file:
			rline += line.replace('\n','\t')
	return rline

if __name__ == '__main__':
	path = "../../data/original_standard_files/"
	new_path = "../../data/converted_standard_files/STANDARD_combined.txt"
	with open(new_path, "w") as new_file:
		for file in os.listdir(path):
			old_path = os.path.join(path, file)
			line = combine_lines(old_path)
			new_file.write(line+'\n')