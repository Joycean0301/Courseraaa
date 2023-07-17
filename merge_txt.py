# Import library
import os
import pandas as pd
import json

# Create dataframe
data = {'Question': [], 'Answer': [], 'Correct': [], 'Title': []}
data_json = []
df = pd.DataFrame(data)

# Create list of question and correct answer for duplicate check
non_duplicate_list = []

# support function
def duplicate_check(question: str, correct_answer: str) -> bool:
    """Check if the question and correct answer are already in the database

    Args:
        question (str): self explanatory
        correct_answer (str): self explanatory

    Returns:
        bool: True if they're in the database, False otherwise
    """

    if len(non_duplicate_list) == 0:
        return False
    for question_answer in non_duplicate_list:
        if question == question_answer[0] and correct_answer == question_answer[1]:
            return True
    return False

# Passing all txt file in folder
list_file_txt = [filename for filename in os.listdir('txt_folder') if '.DS_Store' not in filename]

for ele in list_file_txt:
    # Open txt file
    with open(os.path.join('txt_folder',ele),'r',encoding="latin-1") as file:
        txt_file = file.read()
    
    # Split each question-answer base on @@@
    list_QA = txt_file.split('@@@')


    # Passing all question-answer
    for ele in list_QA:
        info = ele.split('|||')
        
        title, question, answer, correct = info[0], info[1].replace('^^^','\n\n'), info[2].replace('^^^','\n\n'), info[3]

        #check if the question is already in the database
        if duplicate_check(question, correct) == False:
            non_duplicate_list.append([question, correct])
        
            # Update to csv file
            df.loc[len(df)] = [question,answer,correct,title]

            # Update to json file
            temp_dict = {}
            temp_dict.update({'Question':question})
            temp_dict.update({'Answer':answer.split('^^^')})
            temp_dict.update({'Correct':correct.split('^^^')})
            temp_dict.update({'Title':title})
            data_json.append(temp_dict)


file_name = str(input('Input subject name: '))
# Save info to csv file
df.to_csv(os.path.join('csv_folder',f'{file_name}.csv'),index=False)

# Save info to json file
json_file_path = os.path.join('json_folder',f'{file_name}.json')
with open(json_file_path, 'w') as json_file:
    json.dump(data_json, json_file, indent=4)

print('Merge Complete!!!')

print(f'number of questions: {len(non_duplicate_list)}')
