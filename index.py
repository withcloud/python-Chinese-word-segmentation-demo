from snownlp import SnowNLP
import jieba

import argparse
import json

def main(args):
    if args.text:
        # 1. jieba
        r1 = jieba.cut(args.text, cut_all=False)
        # ...

        # 2. snownlp
        r2 = SnowNLP(args.text)

        # final save and print
        # { result1, result2 }
        data = {
            "result1": {
                "words": list(r1)
            },
            "result2": {
                "sentiments": r2.sentiments,
                "words": r2.words,
                "sentiments": r2.sentiments,
            }
        }
        print(data)
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    else:
        print('請輸入文字！')

if __name__ == '__main__':

    parser = argparse.ArgumentParser() 
    parser.add_argument('text', type=str, nargs='?', const='', help='輸入你想說的話')
    parser.add_argument('--model', '-m', default='snownlp', type=str, required=False, help='選擇shownlp（默認）或jieba')
    args = parser.parse_args()

    main(args)
