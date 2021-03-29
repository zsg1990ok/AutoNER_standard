AutoNER基于远程监督的实体识别工具中文适配和电力领域语料应用
增加的文件夹和文件：
1. autoner_train_standard.sh：主体训练脚本，执行读取语料、生成远程监督结果和训练过程；
2. autoner_test_standard.sh：主体测试脚本，执行读取测试集和测试过程；
3. get_ner_pos.py：后处理程序，将输出结果与原始文档形成对应，给出识别的实体和在原始文档中的位置；
4. Standard Preparation文件夹：
  4.1 original_standard_files文件夹：竞赛所用电力变压器37个标准文件经过OCR后导出的txt文本，分段结果还不理想；
  4.2 converted_standard_files文件夹：
    4.2.1 jieba文件夹：对每个标准txt进行结巴分词再按AutoNER要求格式转后的结果，单个文件即为raw_text.txt，_pos为要求格式每行在原始标准txt中的位置，单个文件即为raw_pos.txt；
    4.2.2 single_line文件夹：将每个标准txt转换为一行的结果（本工具未使用）；
  4.3 dictionaries文件夹：三个词库文件power/transformer/mechanic_dictionary.txt，搜狗下载的电力、变压器和机械词库，..segmented.txt，三个词库文件经结巴分词后结果，其中power_dictionary_segmented.txt即为dic_full.txt，一个带类别词库文件，即为dic_core.txt；
  4.4 utils文件夹：
    4.4.1 run_jieba_on_standard.py，输入4.1获得4.2.1；
    4.4.2 run_jieba_on_dict.py，输入4.3词库txt获得segmented.txt；
    4.4.3 toscel.py,将搜狗词库文件scel转为txt；
    4.4.4 prepare_dic_core.py，将两个类别词库拼接获得dic_core.txt；
    4.4.5 和 4.4.6 combine_multiple_files.py和combine_single_file.py，将标准txt转为一行（本工具未使用）。
5. embedding/embedding.txt：更换为中文词向量。
6. data/stopwords.txt：更换为中文停止词。
7. models/STANDARD/result.txt：decoded.txt是AutoNER自身输出结果，本文件是映射到原始标准txt的输出结果，格式为“命名实体tab类别tab原始文件行tab行内起始位置tab终止位置”。

整体使用流程：
1. 执行run_jieba_on_standard.py，获得raw_text.txt和raw_pos.txt；
2. 执行toscel.py、run_jieba_on_dict.py和prepare_dic_core.py，获得dic_full.txt和dic_core.txt;
3. 从 https://pan.baidu.com/s/1XEmP_0FkQwOjipCjI2OPEw 下载word2vec skip-gram negative sampling 300d中文词向量，删除第一行，获得embedding.txt置于embedding文件夹中，从 https://github.com/goto456/stopwords/blob/master/baidu_stopwords.txt 下载baidu_stopwords，替换data文件夹下的stopwords.txt；
4. 执行autoner_train_standard.sh，获得远程监督结果和训练模型；
5.执行autoner_test_standard.sh，获得输出结果和准确率（目前测试集使用远程监督结果）；
6.执行get_ner_pos.py，获得后处理的输出结果。

debug记录：
对原始AutoNER工具的代码做了如下修改，
1. auto_ner_train.sh：修改输出模型文件夹和四个输入文件的路径，将测试集更换为远程监督结果，修改embedding维数为300；
2. auto_ner_test.sh：修改测试路径和embedding维数。
3. encode_folder.py：默认验证集为3段格式，实际用远程监督结果替代所以是4段，修改了代码；
4. dataset.py：ByteTensor在最新PyTorch版本中过时，换为BoolType。

结果和结论：
1. 目前，将远程监督结果作为测试集的F1为0.648。
2. 观察输出结果，实体标注准确率很高，召回率较低，观察远程监督结果，也存在准确率较高但召回率较低的情况。
3. 方法比较有潜力，进一步优化需要提升（1）embedding覆盖的词数，（2）raw_text的规模，（3）dic_core的类别和词数，（4）手工标注一些验证集，帮助模型找到合适的训练停止点。

---------------Original Readme-----------------
# AutoNER

**Check Our New NER Toolkit🚀🚀🚀**
- **Inference**:
  - **[LightNER](https://github.com/LiyuanLucasLiu/LightNER)**: inference w. models pre-trained / trained w. *any* following tools, *efficiently*. 
- **Training**:
  - **[LD-Net](https://github.com/LiyuanLucasLiu/LD-Net)**: train NER models w. efficient contextualized representations.
  - **[VanillaNER](https://github.com/LiyuanLucasLiu/Vanilla_NER)**: train vanilla NER models w. pre-trained embedding.
- **Distant Training**:
  - **[AutoNER](https://shangjingbo1226.github.io/AutoNER/)**: train NER models w.o. line-by-line annotations and get competitive performance.

--------------------------------

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Documentation Status](https://readthedocs.org/projects/autoner/badge/?version=latest)](http://autoner.readthedocs.io/en/latest/?badge=latest)

**No line-by-line annotations**, AutoNER trains named entity taggers with distant supervision.

Details about AutoNER can be accessed at: [https://arxiv.org/abs/1809.03599](https://arxiv.org/abs/1809.03599)

- [Model notes](#model-notes)
- [Benchmarks](#benchmarks)
- [Training](#training)
	- [Required Inputs](#required-inputs)
	- [Dependencies](#dependencies)
	- [Command](#command)
- [Citation](#citation)

## Model Notes

![AutoNER-Framework](docs/AutoNER-Framework.png)

## Benchmarks

| Method | Precision | Recall | F1 |
| ------------- |-------------| -----| -----|
| Supervised Benchmark | 88.84 | 85.16 | **86.96** |
| Dictionary Match | 93.93 | 58.35 | 71.98 |
| Fuzzy-LSTM-CRF | 88.27 | 76.75 | 82.11 |
| AutoNER | 88.96 | 81.00 | **84.80** |

## Training

### Required Inputs

- **Tokenized Raw Texts**
  - Example: ```data/BC5CDR/raw_text.txt```
    - One token per line.
    - An empty line means the end of a sentence.
- **Two Dictionaries**
  - **Core Dictionary w/ Type Info**
    - Example: ```data/BC5CDR/dict_core.txt```
      - Two columns (i.e., Type, Tokenized Surface) per line.
      - Tab separated.
    - How to obtain?
      - From domain-specific dictionaries.
  - **Full Dictionary w/o Type Info**
    - Example: ```data/BC5CDR/dict_full.txt```
      - One tokenized high-quality phrases per line.
    - How to obtain? 
      - From domain-specific dictionaries.
      - Applying the high-quality phrase mining tool on domain-specific corpus.
        - [AutoPhrase](https://github.com/shangjingbo1226/AutoPhrase) 
- **Pre-trained word embeddings**
  - Train your own or download from the web.
  - The example run uses ```embedding/bio_embedding.txt```, which can be downloaded from [our group's server](http://dmserv4.cs.illinois.edu/bio_embedding.txt). For example, ```curl http://dmserv4.cs.illinois.edu/bio_embedding.txt -o embedding/bio_embedding.txt```. Since the embedding encoding step consumes quite a lot of memory, we also provide the encoded file in the ```autoner_train.sh```.
- **[Optional]** Development & Test Sets.
  - Example: ```data/BC5CDR/truth_dev.ck``` and ```data/BC5CDR/truth_test.ck```
    - Three columns (i.e., token, ```Tie or Break``` label, entity type).
    - ```I``` is ```Break```.
    - ```O``` is ```Tie```.
    - Two special tokens ```<s>``` and ```<eof>``` mean the start and end of the sentence.

### Dependencies

This project is based on ```python>=3.6```. The dependent package for this project is listed as below:
```
numpy==1.13.1
tqdm
torch-scope>=0.5.0
pytorch==0.4.1
```

### Command

To train an AutoNER model, please run
```
./autoner_train.sh
```

To apply the trained AutoNER model, please run
```
./autoner_test.sh
```

You can specify the parameters in the bash files. The variables names are self-explained.


## Citation

Please cite the following two papers if you are using our tool. Thanks!

- Jingbo Shang*, Liyuan Liu*, Xiaotao Gu, Xiang Ren, Teng Ren and Jiawei Han, "**[Learning Named Entity Tagger using Domain-Specific Dictionary](https://arxiv.org/abs/1809.03599)**", in Proc. of 2018 Conf. on Empirical Methods in Natural Language Processing (EMNLP'18), Brussels, Belgium, Oct. 2018. (* Equal Contribution)
- Jingbo Shang, Jialu Liu, Meng Jiang, Xiang Ren, Clare R Voss, Jiawei Han, "**[Automated Phrase Mining from Massive Text Corpora](https://arxiv.org/abs/1702.04457)**", accepted by IEEE Transactions on Knowledge and Data Engineering, Feb. 2018.

```
@inproceedings{shang2018learning,
  title = {Learning Named Entity Tagger using Domain-Specific Dictionary}, 
  author = {Shang, Jingbo and Liu, Liyuan and Ren, Xiang and Gu, Xiaotao and Ren, Teng and Han, Jiawei}, 
  booktitle = {EMNLP}, 
  year = 2018, 
}

@article{shang2018automated,
  title = {Automated phrase mining from massive text corpora},
  author = {Shang, Jingbo and Liu, Jialu and Jiang, Meng and Ren, Xiang and Voss, Clare R and Han, Jiawei},
  journal = {IEEE Transactions on Knowledge and Data Engineering},
  year = {2018},
  publisher = {IEEE}
}
```
