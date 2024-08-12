import pandas as pd
import streamlit as st
import re

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
        # Add more validators as needed

    # Calculate validation score for each selected column
    validation_scores = {}
    for column in df.columns:
        if column.startswith('Valid_'):
            validation_scores[column.split('_')[-1]] = df[column].mean() * 100

    # Calculate completeness score for each selected column
    completeness_scores = {}
    for column in df.columns:
        completeness_scores[column] = df[column].notnull().mean() * 100

    validation_results['Validation Score'] = validation_scores
    validation_results['Completeness Score'] = completeness_scores

    return validation_results

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
            validation_results = validate_data(df[selected_columns], selected_validators)

            # Convert validation results to DataFrame
            validation_df = pd.DataFrame(validation_results)
            validation_df.index.name = 'Column'
            st.write('Validation Results:')
            st.write(validation_df)
