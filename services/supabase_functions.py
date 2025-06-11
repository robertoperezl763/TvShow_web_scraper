from typing import (
    List,
    Tuple
)
from supabase import create_client
from config import SUPABASE_KEY, SUPABASE_URL
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def fetchTableID(tableName, column_value_pair: List[Tuple[str, str]], nullable = False) -> None:
  try:
    req = supabase.table(tableName).select('id')
    for column, searchQuery in column_value_pair:
      req = req.eq(column, searchQuery)
    response = req.execute()

    return response.data[0]['id']

  except IndexError as error:
    
    print(f'--Error: Could not find the value ["{searchQuery}"] in column ["{column}"] within the table ["{tableName}"]. Please try again or verify input values')
    print(f'---Error value: {error}')
    return None
  except Exception as e:
    print(f'--Unexpected error when searching for value: ["{searchQuery}"] in column ["{column}"] for table ["{tableName}"].')
    print(f'---Error value: {e}')
    return None


def upsertTableValues(data_to_insert: List[dict], supabase_table_name: str, on_conflict_arg: List[str] = "", ignore_duplicates: bool = True) -> None:
  try:
    response = (
      supabase.table(supabase_table_name)
      .upsert(
        data_to_insert,
        on_conflict = on_conflict_arg,
        ignore_duplicates = ignore_duplicates
      )
      .execute()
    )

    print(f'+++Data Uploaded Successful - In Table ["{supabase_table_name}"]: {response.data}')

    


  except Exception as e:
    print(f'--Ran into unexpected error when attempting to upsert values in table ["{supabase_table_name}"].\n---Error: {e}')
