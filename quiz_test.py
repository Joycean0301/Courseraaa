import pandas as pd
import random 
import os
import time
import json
import argparse

def get_input_choice(len_answer:int,correct_answer:list):
    while True:
        input_chooice_raw = input('Input:')
        input_chooice_list = []
        input_larger = False
        
        if input_chooice_raw == 'hint':
            for ele in (correct_answer):
                print(f'- {ele}')
        
        for i in range(len(input_chooice_raw)):
            try:
                input_chooice_list.append(int(input_chooice_raw[i])-1)
            except:continue
        
        for j in input_chooice_list:
            if j >= len_answer:
                input_larger = True

        
        if (len(input_chooice_raw) == len(input_chooice_list)) and input_larger == False:
            return input_chooice_list
        else:
            if input_chooice_raw != 'hint':
                print('Invalid input')


def main(file_data_path:str,mooc_no:str):
    os.system("clear")

    # Read dataframe
    with open(file_data_path, 'r') as f:
        df = json.load(f)

    #df = pd.read_csv(file_data_path)
    number_of_question = len(df)
    question_list = [i for i in range(number_of_question)]
    random.shuffle(question_list)

    # Define variable
    TIME_START = time.time()
    CORRECT_ANSWER = 0
    INCORRECT_ANSWER = 0
    INDEX_QUESTION = 0
    LIST_WRONG = []
    RED = '\033[91m'
    GREEN = '\033[92m'
    RESET = '\033[0m'
    YELLOW = '\033[93m'

    # Loop through all question
    while len(question_list) != 0:
        question_no = question_list.pop(0)

    # for question_no in question_list:
        temp_row = df[question_no]  #temp row

        question = temp_row['Question']
        list_answer  = temp_row['Answer']   #list
        list_correct = temp_row['Correct']  #list
        random.shuffle(list_answer)

        # show question and answer
        if INDEX_QUESTION+1 > number_of_question:
            COLOR_QUESTION = RED
        else:
            COLOR_QUESTION = GREEN
        print(COLOR_QUESTION + '██ ' + RESET + f'Question: {INDEX_QUESTION+1}/{number_of_question}',GREEN+f'|Correct {CORRECT_ANSWER}'+RESET,RED+f'Incorrect {INCORRECT_ANSWER}'+RESET,YELLOW+f'Left {len(question_list)+1}\n'+RESET)
        print(question)
        print('-'*150)
        for i,ele in enumerate(list_answer):
            print(f'{i+1} - {ele}')
        print('-'*150)
        # for i,ele in enumerate(list_correct):
        #     print(f'{ele}')

        # process correct choice
        list_choose_index = get_input_choice(len_answer=len(list_answer),correct_answer=list_correct)
        list_choose = [list_answer[i] for i in list_choose_index]
        str_correct = ''.join(sorted(''.join(list_correct),reverse=False))
        str_choose  = ''.join(sorted(''.join(list_choose),reverse=False))

        if str_correct == str_choose:
            print(GREEN + "Correct." + RESET)
            CORRECT_ANSWER += 1
        else:
            print(RED + "Incorrect." + RESET)
            INCORRECT_ANSWER += 1
            question_list.append(question_no) #try until correct
            if question_no not in LIST_WRONG:
                LIST_WRONG.append(question_no) #log false question

        INDEX_QUESTION += 1
        time.sleep(1)
        os.system("clear")

    print(        f'Total     : {number_of_question}')       
    print(GREEN + f'Correct   : {CORRECT_ANSWER}' + RESET)
    print(RED   + f'Incorrect : {INCORRECT_ANSWER}' + RESET)
    print(f'{int(time.time()-TIME_START)//60}m{int(time.time()-TIME_START)%60}s')
    
    print('='*71,'LOG','='*74)
    # print log
    dff_wrong = pd.read_csv('output_folder/only-error/data.csv')
    for iii in LIST_WRONG:
        temp_row = df[iii]  #temp row
        question = temp_row['Question']
        list_answer  = temp_row['Answer']   #list
        list_correct = temp_row['Correct'] 
        print(question)
        print('-'*120)
        for i,ele in enumerate(list_answer):
            print(f'{i+1} - {ele}')
        print('-'*120)
        for i,ele in enumerate(list_correct):
            print(f'{ele}')
        print('='*150)
        dff_wrong.loc[len(dff_wrong)] = [mooc_no,temp_row['Question'],temp_row['Answer'],temp_row['Correct']]
    dff_wrong.to_csv('output_folder/only-error/data.csv',index=False)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--data',type=str,default='mooc1')
    args = parser.parse_args()
    main(file_data_path = f'output_folder/{args.data}/data.json',mooc_no=args.data)