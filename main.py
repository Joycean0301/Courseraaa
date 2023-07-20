# Import library
import os
import json
import glob
import logging
import pandas as pd
logging.basicConfig(level=logging.INFO)

def merge_txt():
    """
    Merge all txt file in 'input_folder' into one single file in json and csv format.
    - The json file: use for auto fill question. More details in README.md
    - The csv file: use for store data 
    - The txt_quizlet file: use for create quizlet flashcard. Copy whole file txt and paste to quizlet.
        + Each "Term and Definition" seperate: @@@@@
        + Each "Card" seperate: #####
    """

    # Create Data
    data = {'Question': [], 'Answer': [], 'Correct': [], 'Title': []}
    data_df = pd.DataFrame(data)
    data_json = []
    data_txt = ''


    # Passing all txt file in folder
    txt_file_folder = glob.glob("input_folder/*.txt")
    logging.info(f'Find {len(txt_file_folder)} txt files in input_folder...')
    for txt_path in txt_file_folder:
        with open(txt_path,'r',encoding="utf-8") as file:
            txt_file = file.read()
        
        # Split each question-answer base on @@@
        list_QA = txt_file.split('@@@')

        # Passing all question-answer
        for ele in list_QA:
            info = ele.split('|||')
            title, question, answer, correct = info[0], info[1], info[2].replace('^^^','\n'), info[3].replace('^^^','\n')
            
            # Update to csv file
            data_df.loc[len(data_df)] = [question,answer,correct,title]

            # Update to json file
            temp_dict = {}
            temp_dict.update({'Question':question})
            temp_dict.update({'Answer':answer.split('\n')})
            temp_dict.update({'Correct':correct.split('\n')})
            temp_dict.update({'Title':title})
            data_json.append(temp_dict)

            # Update to txt file
            data_txt += question + '\n' + '-'*20 + '\n' + answer + '@@@@@' + correct + '#####'

    # remove duplicate in dataframe
    data_df['check_duplicate'] = data_df['Question'] + data_df['Answer'] + ['Correct']
    data_df['check_duplicate'] = data_df['check_duplicate'].apply(lambda x: ''.join(sorted(x)))
    data_df.drop_duplicates(subset=['check_duplicate'],inplace=True)
    data_df.drop(columns=['check_duplicate'],inplace=True)

    return data_df, data_json, data_txt


def create_output_folder():
    """
    Create output folder if not exist
    """
    if not os.path.exists('output_folder'):
        os.makedirs('output_folder')
        logging.info('Create output folder.')
    else:
        logging.info('Folder output already exists.')


def save_result(filename, dataframe_data, json_data, txt_quizlet_data):
    """
    Put all data result in the output folder. Move all current txt file to that folder too.
    """
    
    os.makedirs(f'output_folder/{filename}')
    os.makedirs(f'output_folder/{filename}/raw_data') #create folder

    # Save info to csv file
    dataframe_data.to_csv(f'output_folder/{file_name}/data.csv',index=False)

    # Save info to json file
    with open(f'output_folder/{file_name}/data.json', 'w') as json_file:
        json.dump(json_data, json_file, indent=4)
    
    # Save info to txt file
    with open(f'output_folder/{file_name}/data.txt', 'w') as txt_file:
        txt_file.write(txt_quizlet_data)

    # Move data to output_folder
    input_folder = glob.glob('input_folder/*.txt')
    for old_path in input_folder:
        new_path = old_path.replace('input_folder/',f'output_folder/{filename}/raw_data/')
        os.rename(old_path,new_path)
    logging.info('Saving result and moving data...')


if __name__ == "__main__":
    create_output_folder()

    data_df, data_json, data_txt = merge_txt()
    file_name = str(input('Input subject name: '))
    
    save_result(file_name,data_df,data_json,data_txt)
    logging.info('Merge Complete!!!')

