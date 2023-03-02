import logging
from typing import List, Dict, Any
from paddlenlp.transformers import (UnifiedTransformerLMHeadModel,UnifiedTransformerTokenizer)
import yaml              
import os
from termcolor import colored, cprint
from utils import select_response

logger = logging.getLogger(__name__)

# 载入模型配置
yaml_path=os.path.join(os.path.dirname(os.path.abspath(__file__)),"paddle_chat.yml")
# print(yaml_path)
try:
    # 打开文件
    with open(yaml_path,"r",encoding="utf-8") as f:
        conf =yaml.load(f,Loader=yaml.FullLoader)['conf']
except:
    raise Exception("闲聊模型配置文件"+yaml_path+"不存在或存在问题")
logger.info('模型配置已加载')
# print(conf)

# 初始化分词器和模型
tokenizer = UnifiedTransformerTokenizer.from_pretrained(conf['model_name_or_path'])
model = UnifiedTransformerLMHeadModel.from_pretrained(conf['model_name_or_path'])
model.eval()
logger.info('模型加载成功')


def dialog_predict(history: List[str]):
    inputs = tokenizer.dialogue_encode(
        history, add_start_token_as_response=True, return_tensors=True, is_split_into_words=False
    )
    ids, scores = model.generate(
                input_ids=inputs["input_ids"],
                token_type_ids=inputs["token_type_ids"],
                position_ids=inputs["position_ids"],
                attention_mask=inputs["attention_mask"],
                # 以下是yaml中配置的参数
                max_length=conf['max_dec_len'],
                min_length=conf['min_dec_len'],
                decode_strategy=conf['decode_strategy'],
                top_k=conf['top_k'],
                num_return_sequences=conf['num_return_sequences'],
                use_faster=False,
            )
    bot_response = select_response(
        ids, scores, tokenizer, conf['max_dec_len'], conf['min_dec_len'], keep_space=False
    )[0]
    return bot_response
    

if __name__ == '__main__':
    history = []
    start_info = "Enter [EXIT] to quit the interaction, [NEXT] to start a new conversation."
    cprint(start_info, "yellow", attrs=["bold"])
    while True:
        user_utt = input(colored("[Human]: ", "red", attrs=["bold"])).strip()
        if user_utt == "[EXIT]":
            break
        elif user_utt == "[NEXT]":
            history = []
            cprint(start_info, "yellow", attrs=["bold"])
        else:
            history.append(user_utt)
            bot_response = dialog_predict(history)
            print(colored("[Bot]:", "blue", attrs=["bold"]), colored(bot_response, attrs=["bold"]))
            ## hack ## zhw 添加的启发式方法
            if len(history) == 50:
                history = history[25:50]
            if len(history) > 1:
                for i in range(1,len(history)-2):
                    if(bot_response == history[-i]):
                        history = history[0:-i-1]
                        break
            
            ## hack end ##
            history.append(bot_response)