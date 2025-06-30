from load_file import product_dataframe

global df_sorted_by_merchantid,df_sorted_by_productid,df_sorted_by_categoryid
global df_sorted_by_merchantid_productid, df_sorted_by_category_producttitle
def sort_by_merchantid():
#global product_dataframe
    try: 
        if product_dataframe is not None:
            df_sorted_by_merchantid = product_dataframe.sort_values(by='Merchant ID')
            return df_sorted_by_merchantid
    except Exception as e:
            print(f"Data cannot be sorted the DF is empty {e}") 
            return None
def sort_by_productid():
    try: 
        if product_dataframe is not None:
            df_sorted_by_productid = product_dataframe.sort_values(by=['Merchant ID','Product ID'])
            return df_sorted_by_productid
    except Exception as e:
        print(f"Data cannot be sorted the DF is empty {e}") 
        return None

def sort_by_categorylabel():
    try: 
        if product_dataframe is not None:
            df_sorted_by_categoryid = product_dataframe.sort_values(by='Category Label')
            return df_sorted_by_categoryid
    except Exception as e:
        print(f"Data cannot be sorted the DF is empty {e}") 
        return None

def sort_by_merchant_productid():
    try: 
        if product_dataframe is not None:
            df_sorted_by_merchantid_productid = product_dataframe.sort_values(by=['Merchant ID','Product ID'])
            return df_sorted_by_merchantid_productid
    except Exception as e:
        print(f"Data cannot be sorted the DF is empty {e}") 
        return None 
       
def sort_by_categorylabel_producttitle():
    try: 
        if product_dataframe is not None:
            df_sorted_by_category_producttitle = product_dataframe.sort_values(by=['Category Label', 'Product Title'])
            return df_sorted_by_category_producttitle
    except Exception as e:
        print(f"Data cannot be sorted the DF is empty {e}") 
        return None    
 