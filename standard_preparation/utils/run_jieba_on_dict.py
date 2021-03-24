import os
import jieba

def run_jieba(old_path, new_path):
	with open(old_path, "r") as old_file:
		with open(new_path, "w") as new_file:
			for line in old_file:
				words = jieba.cut(line, cut_all=False)
				new_file.write(' '.join(words).strip() + '\n')

if __name__ == '__main__':
	old_path = "../dictionaries/mechanic_dictionary.txt"
	new_path = "../dictionaries/mechanic_dictionary_segmented.txt"
	run_jieba(old_path, new_path)
		