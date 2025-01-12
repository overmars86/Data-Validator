
# Data-Validator

Data-Validator is a Python-based tool that uses Streamlit for validating data in CSV or Excel files. It provides various validators, including custom regex patterns, to ensure data integrity and correctness.

## Features

- Supports CSV and Excel file formats.
- Validates data using built-in validators (Email, EID, Mobile No, Date, DateTime) and custom regex patterns.
- Allows users to select specific columns for validation.
- Displays validation summary and highlights non-valid rows.

## Installation

To install the required dependencies, run:
```bash
pip install pandas streamlit
```

## Usage

To run the Data-Validator application, execute the following command:
```bash
streamlit run final.py
```

## How It Works

1. **Upload File**: Upload a CSV or Excel file.
2. **Select Columns**: Choose the columns you want to validate.
3. **Define Validators**: Select appropriate validators for each column or provide custom regex patterns.
4. **Run Validator**: Click the "Run Validator" button to validate the data.
5. **View Results**: See the validation summary and inspect non-valid rows if any.

## Example

```python
import pandas as pd
import streamlit as st
import re
from datetime import datetime, date

def validate_data(df, validators):
    validation_results = {}
    for column, validator in validators.items():
        if validator == 'Custom':
            custom_pattern = st.session_state[f'custom_validator_{column}']
            if custom_pattern:
                df[f'Valid_{column}'] = df[column].astype(str).apply(lambda x: bool(re.match(custom_pattern, str(x))))
        elif validator == 'Email':
            df[f'Valid_{column}'] = df[column].astype(str).apply(lambda x: bool(re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', str(x))))
        elif validator == 'EID':
            df[f'Valid_{column}'] = df[column].astype(str).apply(lambda x: bool(re.match(r'^[0-9]+-[0-9]+-[0-9]+-\d$', str(x))))
        elif validator == 'Mobile No':
            df[f'Valid_{column}'] = df[column].astype(str).apply(lambda x: bool(re.match(r'\d\d\d-\d\d\d\d\d\d\d', str(x))))
        elif validator == 'Date':
            df[column] = pd.to_datetime(df[column], errors='coerce').dt.date
            df[f'Valid_{column}'] = (df[column] >= date.today())
        elif validator == 'DateTime':
            df[column] = pd.to_datetime(df[column], errors='coerce')
            df[f'Valid_{column}'] = df[column].notnull()
        elif validator is None: 
            df[f'Valid_{column}'] = True 
    return df

st.title('Data Validator')
uploaded_file = st.file_uploader('Upload CSV or Excel file', type=['csv', 'xlsx'])

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
    except Exception as e:
        st.error(f'Error reading file: {str(e)}')
    else:
        st.write('Original DataFrame:')
        st.write(df)
        selected_columns = st.multiselect('Select columns to work with', df.columns)
        custom_validators = {}
        for column in selected_columns:
            custom_pattern = st.text_input(f'Enter custom regex pattern for column "{column}"')
            if custom_pattern:
                custom_validators[column] = custom_pattern
        validators = {'None': None, 'Email': 'Email', 'EID': 'EID', 'Mobile No': 'Mobile No', 'Date': 'Date', 'DateTime': 'DateTime', 'Custom': 'Custom'}
        selected_validators = {}
        for column in selected_columns:
            validator = st.selectbox(f'Select validator for column "{column}"', list(validators.keys()))
            selected_validators[column] = validators[validator]
            if validator == 'Custom':
                st.session_state[f'custom_validator_{column}'] = custom_validators[column]
        if st.button('Run Validator'):
            df_validated = validate_data(df[selected_columns], selected_validators)
            validation_results = pd.DataFrame()
            for column, validator in selected_validators.items():
                validation_results.loc['Validation Score', column] = df_validated[f'Valid_{column}'].mean() * 100
                validation_results.loc['Completeness Score', column] = df_validated[column].notnull().mean() * 100
            st.write('Validation Summary:')
            st.write(validation_results)
            non_valid_rows = df_validated[~df_validated[[col for col in df_validated.columns if col.startswith('Valid_')]].all(axis=1)]
            if not non_valid_rows.empty:
                st.write('Filtered Dataset (Non-Valid Rows Only):')
                st.write(non_valid_rows)
            else:
                st.write('No non-valid rows found.')
```

## License

This project is licensed under the MIT License.

## Contributing

Feel free to fork this repository and contribute by submitting pull requests.

## Contact

For any questions or suggestions, please open an issue or contact [overmars86](https://github.com/overmars86).


