import linecache

if __name__ == "__main__":
	ner_path = "./models/STANDARD/decoded.txt"
	text_path = "./data/STANDARD/raw_text.txt"
	pos_path = "./data/STANDARD/raw_pos.txt"
	res_path = "./models/STANDARD/result.txt"
	print("working...")
	with open(ner_path, 'r') as ner_file:
		with open(res_path, 'w') as res_file:
			for line in ner_file:
				line = line.strip().split('\t')
				if len(line) == 5:
					sln, eln, surface, _, type = line
					if type != 'None':
						rln, rs, _ = linecache.getline(pos_path, int(sln) + 1).split()
						re = linecache.getline(pos_path, int(eln)).split()[2]
						res_file.write(surface + '\t' + type + '\t' + rln + '\t' + rs + '\t' + re + '\n')
