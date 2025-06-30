import pandas as pd
import os

global product_dataframe
 
def load_file():
        #Hard codign file path 
        file_path ="C:\MAC-WilfredLaurier\CP612-DataManagementAnalysis\product+classification+and+clustering\pricerunner_aggregate_original.csv" 
        
        if not os.path.exists(file_path):
            print(f"File path {file_path} does not exists")
        try: 
            global  product_dataframe 
            product_dataframe= pd.read_csv(file_path, low_memory= False)
            return product_dataframe
        except pd.errors.EmptyDataError:
            print(f"Error: The CSV file '{file_path}' is empty.")
            return None
        except pd.errors.ParserError as e:
            print(f"Error parsing CSV file '{file_path}': {e}")
            print("This might be due to malformed rows, incorrect delimiters, or encoding issues.")
            return None
        except Exception as e:
            print(f"An unexpected error occurred while reading the file: {e}")
            return None
       














