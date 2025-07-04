#from load_file import product_dataframe
from source_data import load_file #fixed so that python can find product_dataframe in load_file

global df_sorted_by_merchantid,df_sorted_by_productid,df_sorted_by_categoryid
global df_sorted_by_merchantid_productid, df_sorted_by_category_producttitle
def sort_by_merchantid(df):
#global product_dataframe
    try: 
        if df is not None:
            df_sorted_by_merchantid = df.sort_values(by='Merchant ID')
            return df_sorted_by_merchantid
    except Exception as e:
            print(f"Data cannot be sorted the DF is empty {e}") 
            return None
def sort_by_productid(df): # added parameter "df" (dataframe) - which is a reference to the global product_dataframe
    try: 
        if df is not None:
            df_sorted_by_productid = df.sort_values(by=['Merchant ID','Product ID'])
            return df_sorted_by_productid
    except Exception as e:
        print(f"Data cannot be sorted the DF is empty {e}") 
        return None

def sort_by_categorylabel(df):
    try: 
        if df is not None:
            df_sorted_by_categoryid = df.sort_values(by='Category Label')
            return df_sorted_by_categoryid
    except Exception as e:
        print(f"Data cannot be sorted the DF is empty {e}") 
        return None

def sort_by_merchant_productid(df):
    try: 
        if df is not None:
            df_sorted_by_merchantid_productid = df.sort_values(by=['Merchant ID','Product ID'])
            return df_sorted_by_merchantid_productid
    except Exception as e:
        print(f"Data cannot be sorted the DF is empty {e}") 
        return None 
       
def sort_by_categorylabel_producttitle(df):
    try: 
        if df is not None:
            df_sorted_by_category_producttitle = df.sort_values(by=['Category Label', 'Product Title'])
            return df_sorted_by_category_producttitle
    except Exception as e:
        print(f"Data cannot be sorted the DF is empty {e}") 
        return None    

# GS _ i added a generic sorter - so we can try sorting by every combination to see what it does. 
# However, I don't think it's the sort that matters, unless we also assign a key based on the sort order
def sort_by_attribute (df, sort_attributes):
    # attributes is a string value or list of strings
    try:
        if df is not None:
            column_names = list(df.columns)
            for attribute in sort_attributes:
                if attribute not in column_names:
                    print(f'Error no column {attribute}')
                    return None
            sorted_df = df.sort_values(by=sort_attributes)
            return sorted_df
    except Exception as e:
        print(f"Data cannot be sorted the DF is empty {e}") 
        return None    
            
 