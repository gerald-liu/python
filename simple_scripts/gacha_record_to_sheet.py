import pandas as pd

def text_to_df(in_file):
    with open(in_file, encoding='utf-8') as f:
        str_input = f.read()
    
    if not str_input:
        return pd.DataFrame()
    
    list_records = str_input.split(' ')
    
    list_2d_records = []

    for str_record in list_records:
        name, num = str_record.split('[')
        num = int(num.replace(']', ''))
        list_2d_records.append([name, num])

    return pd.DataFrame(list_2d_records, columns=['Name','Num'])


def df_to_sheet(df, sheet, writer):
    if df.empty:
        return
    df.to_excel(writer, sheet_name=sheet, index=False)


with pd.ExcelWriter('./out.xlsx', engine='openpyxl') as writer:
    df_to_sheet(text_to_df('./character_event.txt'), 'Char', writer)
    df_to_sheet(text_to_df('./light_cone_event.txt'), 'LC', writer)
    df_to_sheet(text_to_df('./regular.txt'), 'Reg', writer)
