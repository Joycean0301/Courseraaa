from pynput import keyboard
from pynput.keyboard import Key
import pandas as pd
import os
import sys
import random
import argparse
import json


def save_content(question:int, title:str):
    global CORRECT,ANSWER,df,GREEN,RESET,RED
    os.system("clear")
    #row = df.iloc[question]
    row = df[question]
    temp_answer = ''
    temp_correct = ''

    temp_answer += (f'Question: {question+1}/{len(df)} | {title}\n') + '-'*130 +'\n'
    temp_answer += (row['Question']) + '\n'
    temp_answer += ('-'*130) + '\n'

    temp_correct += (f'Question: {question+1}/{len(df)} | {title}\n') + '-'*130 +'\n'
    temp_correct += (row['Question']) + '\n'
    temp_correct += ('-'*130) + '\n'

    # answerr = row['Answer'].split('\n\n')
    answerr = row['Answer']
    random.shuffle(answerr)
    for ele in (answerr):
        temp_answer += (f'- {ele}') + '\n'
        
        # if ele in str(row['Correct']).split('\n\n'):
        if ele in row['Correct']:
            temp_correct += GREEN+(f'- {ele}') + '\n'+RESET
        else:
            temp_correct += RED+(f'- {ele}') + '\n'+RESET
    
    temp_answer += ('-'*130) +'\n'
    temp_correct += ('-'*130) +'\n'

    ANSWER = temp_answer
    CORRECT = temp_correct
       

def on_key_release(key):
    global QUESTION,CORRECT,ANSWER,df,title_data,FLIP
    # if key == Key.right:
    if key == Key.right:
        QUESTION+=1
        if QUESTION == len(df):
            QUESTION = 0
        save_content(QUESTION,title_data)
        print(ANSWER)
        FLIP = True
    # elif key == Key.left:
    elif key == Key.left:
        QUESTION-=1
        save_content(QUESTION,title_data)
        print(ANSWER)
        FLIP = True
    # elif key == Key.down:
    elif (key == Key.space or key == Key.down) and FLIP == True:
        os.system("clear")
        print(CORRECT)
        FLIP = False
    # elif key == Key.up:
    elif (key == Key.space or key == Key.up) and FLIP == False:
        os.system("clear")
        print(ANSWER)
        FLIP = True
    elif key == Key.esc:
        exit()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--data',type=str,default='mooc1')
    args = parser.parse_args()
    

    #df = pd.read_csv(f'output_folder/{args.data}/data.csv')
    file_name = f'output_folder/{args.data}/data.json'
    with open(file_name, 'r') as f:
        df = json.load(f)
    
    QUESTION = 0
    ANSWER = ''
    CORRECT = ''
    GREEN = '\033[92m'
    RED = '\033[91m'
    RESET = '\033[0m'
    FLIP = True
    title_data = args.data

    save_content(QUESTION,title_data)
    print(ANSWER)
    with keyboard.Listener(on_release=on_key_release) as listener:
        listener.join()