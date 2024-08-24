import fitparse

# Step 1: Parse the .fit file
fitfile = fitparse.FitFile('../data/session.fit')

# Step 2: Initialize a set to keep track of all data fields
all_data_fields = set()

# Step 3: Iterate through the records and extract data fields
for record in fitfile.get_messages('record'):
    record_data = record.header

    # Add the keys of the record_data dictionary to the all_data_fields set
    all_data_fields.update(record_data.keys())

    # For demonstration, print the values in each record
    print("Record data:")
    for key, value in record_data.items():
        print(f"  {key}: {value}")
    print("-" * 40)

# Step 4: Print out all unique data fields found in the .fit file
print("Available data fields:")
for field in all_data_fields:
    print(f"  {field}")
