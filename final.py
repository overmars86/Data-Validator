import pandas as pd
import streamlit as st
import re
from datetime import datetime, date

# Function to validate data based on selected validators
def validate_data(df, validators):
    validation_results = {}

    # Apply validators to selected columns
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
        elif validator is None:  # Handle columns with None validator
            df[f'Valid_{column}'] = True  # All values are considered valid for completeness
        # Add more validators as needed

    return df

# Streamlit UI
st.title('Data Validator')

# File upload
uploaded_file = st.file_uploader('Upload CSV or Excel file', type=['csv', 'xlsx'])

if uploaded_file is not None:
    # Read the uploaded file
    try:
        df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
    except Exception as e:
        st.error(f'Error reading file: {str(e)}')
    else:
        # Display DataFrame
        st.write('Original DataFrame:')
        st.write(df)

        # Select columns to work with
        selected_columns = st.multiselect('Select columns to work with', df.columns)

        # Allow user to add custom validator
        custom_validators = {}
        for column in selected_columns:
            custom_pattern = st.text_input(f'Enter custom regex pattern for column "{column}"')
            if custom_pattern:
                custom_validators[column] = custom_pattern

        # Define validators
        validators = {
            'None': None,
            'Email': 'Email',
            'EID': 'EID',
            'Mobile No': 'Mobile No',
            'Date': 'Date',
            'DateTime': 'DateTime',
            'Custom': 'Custom',
            # Add more validators here
        }

        # Assign validator for each column
        selected_validators = {}
        for column in selected_columns:
            validator = st.selectbox(f'Select validator for column "{column}"', list(validators.keys()))
            selected_validators[column] = validators[validator]

            # Store custom validator pattern in session state
            if validator == 'Custom':
                st.session_state[f'custom_validator_{column}'] = custom_validators[column]

        if st.button('Run Validator'):
            # Validate the data
            df_validated = validate_data(df[selected_columns], selected_validators)

            # Display validation summary
            validation_results = pd.DataFrame()
            for column, validator in selected_validators.items():
                validation_results.loc['Validation Score', column] = df_validated[f'Valid_{column}'].mean() * 100
                validation_results.loc['Completeness Score', column] = df_validated[column].notnull().mean() * 100

            st.write('Validation Summary:')
            st.write(validation_results)

            # Display non-valid rows
            non_valid_rows = df_validated[~df_validated[[col for col in df_validated.columns if col.startswith('Valid_')]].all(axis=1)]

            if not non_valid_rows.empty:
                st.write('Filtered Dataset (Non-Valid Rows Only):')
                st.write(non_valid_rows)
            else:
                st.write('No non-valid rows found.')
