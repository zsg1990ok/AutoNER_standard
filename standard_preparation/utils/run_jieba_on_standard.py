import os
import jieba

def run_jieba(old_path, new_path):
	with open(old_path, "r") as old_file:
		with open(new_path, "w") as new_file:
			for line in old_file:
				words = jieba.cut(line, cut_all=False)
				new_file.write('\n'.join([w for w in words if w.strip() != '']) + '\n\n')

if __name__ == '__main__':
	original_path = "../../data/original_standard_files/"
	converted_path = "../../data/converted_standard_files/jieba"
	for file in os.listdir(original_path):
		old_path = os.path.join(original_path, file)
		new_path = os.path.join(converted_path, file)
		run_jieba(old_path, new_path)
		