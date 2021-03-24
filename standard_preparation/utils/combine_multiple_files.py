import os

def combine_lines(old_path):
	rline = ""
	with open(old_path, "r") as old_file:
		for line in old_file:
			if line.strip() != '':
				rline += line.strip() + '\t'
	return rline.rstrip()

if __name__ == '__main__':
	path = "../original_standard_files/"
	new_path = "../converted_standard_files/single_line/combined.txt"
	with open(new_path, "w") as new_file:
		for file in os.listdir(path):
			old_path = os.path.join(path, file)
			line = combine_lines(old_path)
			new_file.write(line + '\n')