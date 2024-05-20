# Import library
import os
import json
import glob
import logging
import pandas as pd
import argparse
import sys
logging.basicConfig(level=logging.INFO)


def merge_txt(history_row = None):
    """Merge all txt file in 'input_folder' into one single file in json and csv format.
    - The json file: use for auto fill question. More details in README.md
    - The csv file: use for store data 
    - The txt_quizlet file: use for create quizlet flashcard. Copy whole file txt and paste to quizlet.
        + Each "Term and Definition" seperate: @@@@@
        + Each "Card" seperate: #####

    Returns:
        data_df (pd.DataFrame): Data (contain question, answers, correct answer) in csv format.
        data_json (json): Data in csv format.
        data_txt (txt): Data in csv format, use for making flashcard.
    """

    # Define variable
    json_file_folder = sorted(glob.glob("input_folder/*.json"),reverse=False)
    logging.info(f'Find {len(json_file_folder)} json files in input_folder...')
    df_structure = {'Question': [], 'Answer': [], 'Correct': [], 'Title': []}
    seen_value = set()  # Track seen names
    DATA_DF = pd.DataFrame(df_structure)
    DATA_TXT = ''
    DATA_JSON = []  # Create a new list to store unique objects

    # Loop through all json file too merge it all together
    for json_path in json_file_folder:
        # Load data from JSON file
        with open(json_path, "r") as file:
            json_file_data = json.load(file)

        # Iterate through each object in the original data
        for obj in json_file_data:
            identity_value = ''.join(sorted(obj['Question'] + ''.join(obj['Answer']) + ''.join(obj['Correct']),reverse=False))
            if identity_value not in seen_value: # filter duplicate items
                if (len(obj['Question']) != 0) and (len(''.join(obj['Answer'])) != 0) and (len(''.join(obj['Correct'])) != 0): # filter empty question
                    DATA_JSON.append(obj)
                    seen_value.add(identity_value)

    # Update data to txt and dataframe
    for object in DATA_JSON:
        DATA_TXT += object['Question'] + '\n' + '-'*20 + '\n' + '\n'.join(object['Answer']) + '@@@@@' + '\n'.join(object['Correct']) + '#####'
        DATA_DF.loc[len(DATA_DF)] = [object['Question'],'\n'.join(object['Answer']),'\n'.join(object['Correct']),object['Title']]
    # Loggin the change
    if history_row == None:
        logging.info(f'Add new {len(DATA_DF)} questions in dataset')
    else:
        logging.info(f'Upgrade {history_row} -> {len(DATA_DF)} questions in dataset')
    

    return DATA_DF, DATA_JSON, DATA_TXT


def create_output_folder():
    """create output folder to store data if not exist
    """
    if not os.path.exists('output_folder'):
        os.makedirs('output_folder')
        logging.info('Create output folder.')
    else:
        logging.info('Folder output already exists.')


def check_recreate(name:str):
    """check if mooc exist or not
          - if yes: move data back to update
          - if no: do nothing

    Args:
        name (str): path of current data
    """
    if name is None:
        logging.info('Argument --name is empty...')
        sys.exit()
    elif name in os.listdir('output_folder'):
        # move all json file to input_folder
        input_folder = glob.glob(f'output_folder/{name}/raw_data/*.json')
        for old_path in input_folder:
            new_path = old_path.replace(f'output_folder/{name}/raw_data/','input_folder/')
            os.rename(old_path,new_path)

        # log past num question
        history_rows = int(len(pd.read_csv(f'output_folder/{name}/data.csv')))

        # delete folder
        os.remove(f'output_folder/{name}/data.csv')
        os.remove(f'output_folder/{name}/data.txt')
        os.remove(f'output_folder/{name}/data.json')
        os.rmdir(f'output_folder/{name}/raw_data')
        os.rmdir(f'output_folder/{name}')
        logging.info('Mooc exist, re-create mooc')
        return history_rows
    else:
        logging.info('Creating new mooc')
        return None


def save_result(filename, dataframe_data, json_data, txt_quizlet_data):
    """save data to output folder

    Args:
        filename (str): name of the course.
        dataframe_data (pd.DataFrame): Data in dataframe format.
        json_data (json): Data in json format.
        txt_quizlet_data (txt): Data in txt format.
    """
    
    os.makedirs(f'output_folder/{filename}')
    os.makedirs(f'output_folder/{filename}/raw_data') #create folder

    # Save info to csv file
    dataframe_data.to_csv(f'output_folder/{filename}/data.csv',index=False)

    # Save info to json file
    with open(f'output_folder/{filename}/data.json', 'w') as json_file:
        json.dump(json_data, json_file, indent=4)
    
    # Save info to txt file
    with open(f'output_folder/{filename}/data.txt', 'w') as txt_file:
        txt_file.write(txt_quizlet_data)

    # Move data to output_folder
    input_folder = glob.glob('input_folder/*.json')
    for old_path in input_folder:
        new_path = old_path.replace('input_folder/',f'output_folder/{filename}/raw_data/')
        os.rename(old_path,new_path)
    logging.info('Saving result and moving data...')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='get input data from source')
    parser.add_argument('--name',type=str,default="AIE301m")
    args = parser.parse_args()

    create_output_folder()
    history_row = check_recreate(args.name)
    
    data_df, data_json, data_txt = merge_txt(history_row=history_row)
    
    save_result(filename=args.name,
                dataframe_data=data_df,
                json_data=data_json,
                txt_quizlet_data=data_txt)
    logging.info('Merge Complete!!!')


