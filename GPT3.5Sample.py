import openai
import random
import re

sig_dic={0:[' |<.*?>',''], 1:['…+','……'], 2:['"\!+','!'], 3:['"\?+','?'], 4:['。+','。'], 5:['、+','、']}
Termination_sig = ["！", "？", "!", "?", "。", "、", "!?", "?!"] #[4]まで：句点、[5]まで：句読点

def completion(input_text:str, settings:str = '', past_turns:list = []):
    """
    This function generates a response message using OpenAI's GPT-3 model by taking in a new message text, 
    optional settings text and a list of past messages as inputs.

    Args:
    new_message_text (str): The new message text which the model will use to generate a response message.
    settings_text (str, optional): The optional settings text that will be added as a system message to the past_messages list. Defaults to ''.
    past_messages (list, optional): The optional list of past messages that the model will use to generate a response message. Defaults to [].

    Returns:
    tuple: A tuple containing the response message text and the updated list of past messages after appending the new and response messages.
    """
    target_massages = []
    target_massages.append({"role": "system", "content": settings})
    for past_tests in past_turns:
        target_massages.append({"role": "user", "content": past_tests[0]})
        target_massages.append({"role": "assistant", "content": past_tests[1]})
    target_massages.append({"role": "user", "content": input_text})
    result = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        max_tokens = 50,
        messages=target_massages
    )
    response_message_text = result.choices[0].message.content
    return response_message_text, target_massages

openai.api_key = "" #OpenAI API Key
past_text=[["よろしく。","よろしくお願いします。"]]
print(past_text[-1][1])
while True:
    input_text = input()
    texts_path="sample.txt"
    md = [s.strip() for s in open(texts_path, encoding = "utf-8").readlines()]
    emotion_text = "User dislikes you and You like user." #ユーザ・システムの感情状態
    task1 = "Pretend to be a girl named あかり and respond frankly to user (ぐでたま). Refer to the following samples.\n" #タスクの例示。ユーザ・システム名を明示
    sample_text = "\n".join(random.sample(md,10)) #サンプルテキストファイルから10個重複なしで選出
    task2 = emotion_text+" Answer the question with words that answer the question. The following are conversational texts." #感情情報と禁則事項への対応
    task_text = task1+sample_text+task2
    for i, _ in enumerate(sig_dic):
        task_text = re.sub(sig_dic[i][0],sig_dic[i][1], task_text)
    output_text, messages = completion(input_text, task_text, past_text)
    result = outputList
    print(result)
    if len(past_text) == 5: del past_text[0]
    past_text.append([input_text,result])
