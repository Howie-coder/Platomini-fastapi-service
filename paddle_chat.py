import logging
from typing import List, Dict, Any
# from paddlenlp.transformers import (UnifiedTransformerLMHeadModel,UnifiedTransformerTokenizer)
import yaml              
import os

logger = logging.getLogger(__name__)

# 载入模型配置
yaml_path=os.path.join(os.path.dirname(os.path.abspath(__file__)),"paddle_chat.yml")
print(yaml_path)

try:
    # 打开文件
    with open(yaml_path,"r",encoding="utf-8") as f:
        conf =yaml.load(f,Loader=yaml.FullLoader)
except:
    raise Exception("闲聊模型配置文件损坏")
logger.info('模型配置已加载')
print(conf)
exit()
# 初始化分词器和模型
tokenizer = UnifiedTransformerTokenizer.from_pretrained('plato-mini')
model = UnifiedTransformerLMHeadModel.from_pretrained('plato-mini')
model.eval()
logger.info('模型加载成功')


def dialog_predict(
    history: List[str],
    **kwargs: Dict[str, Any]
) -> str:
    """
    Predict the next dialog utterance.

    Args:
      history: A list of dialog utterances.
      **kwargs: Additional keyword arguments.

    Returns:
      The predicted dialog utterance.
    """

    inputs = tokenizer.dialogue_encode(
        history,
        add_start_token_as_response=True,
        return_tensors=True,
        is_split_into_words=False
    )

    output_ids, score = model.generate(
        **inputs,
        **kwargs,
    )

    token_ids = output_ids.numpy()[0]

    eos_pos = len(token_ids)
    for i, tok_id in enumerate(token_ids):
        if tok_id == tokenizer.sep_token_id:
            eos_pos = i
            break
    token_ids = token_ids[:eos_pos]
    tokens = tokenizer.convert_ids_to_tokens(token_ids)
    tokens = tokenizer.merge_subword(tokens)

    return ''.join(tokens)

if __name__ == '__main__':
    history = ['你好！']
    print(dialog_predict(history))