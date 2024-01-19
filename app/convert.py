import argparse
import pandas as pd

def convert_to_excel(input_file, output_file):
    try:
        if input_file.endswith('.csv'):
            df = pd.read_csv(input_file)
        elif input_file.endswith('.txt'):
            df = pd.read_csv(input_file, delimiter='\t')
        else:
            raise ValueError("Unsupported input file format. Only .csv and .txt files are supported.")

        # Write the DataFrame to an Excel file
        df.to_excel(output_file, index=False)
        print(f"Conversion successful. Excel file saved as {output_file}")
    except Exception as e:
        print(f"Conversion failed: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description="Convert CSV and text files to Excel")
    parser.add_argument("input_file", help="Input CSV or text file")
    parser.add_argument("output_file", help="Output Excel file")
    args = parser.parse_args()

    convert_to_excel(args.input_file, args.output_file)

if __name__ == "__main__":
    main()