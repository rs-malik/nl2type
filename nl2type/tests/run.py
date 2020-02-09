from nl2type import convert
from nl2type import extract
import pandas as pd


def run(js_files_dir):
    pd.set_option('display.max_colwidth', -1)
    pd.set_option('display.max_columns', 500)
    extracted_jsdoc = extract.extract_from_dir(js_files_dir)
    df = convert.convert_func_to_df(extracted_jsdoc)

    print(df)


if __name__ == '__main__':
    run("/home/rabee/projects/nl2type/nl2type/data/input")
