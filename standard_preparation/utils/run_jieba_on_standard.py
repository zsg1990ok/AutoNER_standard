import os
import jieba

def run_jieba(old_path, new_path, pos_path):
	with open(old_path, "r") as old_file:
		with open(new_path, "w") as new_file:
			with open(pos_path, "w") as pos_file:
				ln = 1
				for line in old_file:
					sp = 0
					ep = 0
					words = list(jieba.cut(line, cut_all=False))
					bl = True
					for w in words:
						ep = sp + len(w) - 1
						if w.strip() != '':
							new_file.write(w + '\n')
							pos_file.write(str(ln) + '\t' + str(sp) + '\t' + str(ep) + '\n')
							bl = False
						sp = ep + 1
					ln += 1
					if not bl:
						new_file.write('\n')
						pos_file.write('\n')

if __name__ == '__main__':
	original_path = "../original_standard_files/"
	converted_path = "../converted_standard_files/jieba/"
	for file_name in os.listdir(original_path):
		old_path = original_path + file_name
		new_path = converted_path + file_name
		pos_path = converted_path + os.path.splitext(file_name)[0] + "_pos.txt" 
		run_jieba(old_path, new_path, pos_path)
		