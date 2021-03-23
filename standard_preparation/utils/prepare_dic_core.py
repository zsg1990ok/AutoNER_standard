if __name__ == '__main__':
	dic1_path = "../../data/dictionaries/transformer_dictionary_segmented.txt"
	dic2_path = "../../data/dictionaries/mechanic_dictionary_segmented.txt"
	diccore_path= "../../data/dictionaries/dic_core.txt"
	dic1 = set()
	dic2 = set()
	with open(diccore_path, 'w') as diccore_file:
		with open(dic1_path, 'r') as dic1_file:
			for line in dic1_file:
				dic1.add(line.strip())
		with open(dic2_path, 'r') as dic2_file:
			for line in dic2_file:
				dic2.add(line.strip())
		dic3 = dic2.difference(dic1)
		for w in dic1:
			diccore_file.write("transformer"+ '\t' + w + '\n')
		for w in dic3:
			diccore_file.write("mechanic"+ '\t' + w + '\n')