import pandas as pd
import os

unique_values = None
#global product_dataframe  GS - removed, as it's redundant - you have this in line 15, where it belongs
 
def load_file():
        #Hard coding file path 
        #file_path ="C:\MAC-WilfredLaurier\CP612-DataManagementAnalysis\product+classification+and+clustering\pricerunner_aggregate_original.csv" 
        # GS - I put data file in same folder as this code and made relative path
        file_path = os.path.join(os.path.dirname(__file__), 'pricerunner_aggregate.csv')
    
        if not os.path.exists(file_path):
            print(f"File path {file_path} does not exists")
        try: 
            global  product_dataframe 
            product_dataframe= pd.read_csv(file_path, low_memory= False)
            product_dataframe.columns = product_dataframe.columns.str.strip()  #added because leading spaces in the csv cause issues
            global unique_values
            unique_values = UniqueValues(product_dataframe)
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


class UniqueValues:
    # GS - added this to allow us to test searches for specific values without duplication
    def __init__(self, df):
        self.merchant_id = sorted(set(df['Merchant ID'].dropna().unique()))
        self.category_id = sorted(set(df['Category ID'].dropna().unique()))
        self.cluster_id = sorted(set(df['Cluster ID'].dropna().unique()))
        self.product_id = sorted(set(df['Product ID'].dropna().unique()))
        self.product_title = sorted(set(df['Product Title'].dropna().unique()))
        self.cluster_label = sorted(set(df['Cluster Label'].dropna().unique()))
        self.category_label = sorted(set(df['Category Label'].dropna().unique()))

    def get_merchant_id(self): return self.merchant_id
    def get_category_id(self): return self.category_id
    def get_cluster_id(self): return self.cluster_id
    def get_product_id(self): return self.product_id
    def get_product_title(self): return self.product_title
    def get_cluster_label(self): return self.cluster_label
    def get_category_label(self): return self.category_label






