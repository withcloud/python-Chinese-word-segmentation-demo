from stopwordsiso import stopwords
from snownlp import SnowNLP
import jieba
import opencc


import argparse
import json

import re

def eliminate_duplicates_output(text):
    return re.sub(r'(.)\1+', r'\1\1', text)

def eliminate_numbers_output(text):
    return re.sub(r'[0-9]', r'', text)

def jieba_output(text):
    # return {
    #     "words": list(jieba.cut(text, cut_all=False))
    # }
    return list(jieba.cut(text, cut_all=False))

def eliminate_modifiers_output(text_arr):
    stopwords_list = stopwords(['en', 'zh'])
    return [x for x in text_arr if x not in stopwords_list]

def textArr_merge(text_arr):
    return ' '.join(text_arr)

def snownlp_output(text):
    item = SnowNLP(text)
    return {
        "sentiments": item.sentiments,
        "words": item.words
    }

def opencc_output(text):
    # s2t.json Simplified Chinese to Traditional Chinese 簡體到繁體
    # t2s.json Traditional Chinese to Simplified Chinese 繁體到簡體
    converter = opencc.OpenCC('s2t.json')
    converter2 = opencc.OpenCC('t2s.json')
    return {
        "traditional-Chinese": converter.convert(text),
        "simplified-Chinese": converter2.convert(text)
    }

def main(args):
    if args.text:
        # 0-1. 消除重複的字
        text = eliminate_duplicates_output(args.text)
        # 0-2. 消除數字
        text = eliminate_numbers_output(text)

        # 1. jieba進行分詞
        text_arr = jieba_output(text)

        # 2. 消除修飾詞
        text_arr = eliminate_modifiers_output(text_arr)

        # 3. 合併成字串
        text = textArr_merge(text_arr)

        # 2. snownlp
        r2 = snownlp_output(text)

        # 3. opencc
        r3 = opencc_output(text)

        # final save and print
        # { result1, result2, 繁體, 簡體  }
        data = {
            "result2": {**r2},
            **r3,
        }
        print(data)
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    else:
        print({"result2":{}})

if __name__ == '__main__':

    parser = argparse.ArgumentParser() 
    parser.add_argument('text', type=str, nargs='?', const='', help='輸入你想說的話')
    parser.add_argument('--model', '-m', default='snownlp', type=str, required=False, help='選擇shownlp（默認）或jieba')
    args = parser.parse_args()

    main(args)
