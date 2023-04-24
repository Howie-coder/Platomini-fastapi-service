from paddle_chat import dialog_predict
import api

# 只需导入接受List[str],返回str的函数初始化api.ChatAgentAPI
# 再调用run方法即可
if __name__ == "__main__":
    agent = api.ChatAgentAPI(dialog_predict_func=dialog_predict)
    agent.run(port=9000)