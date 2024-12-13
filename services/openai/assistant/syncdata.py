from openai import OpenAI
import pandas as pd

# Initialize OpenAI client
client = OpenAI()

# Model for data generation
datagen_model = "gpt-4o-mini"

# Question to generate data
question = """
Create a CSV file with 20 rows of housing data.
Each row should include the following fields:
 - id (incrementing integer starting at 1, number must be unique)
 - house size (m^2)
 - house price
 - location
 - race of the owner
 - number of bedrooms
  - number of bathrooms
  - number of floors

Make sure that the numbers make sense (i.e. more rooms is usually bigger size, more expensive locations increase price. more size is usually higher price etc. make sure all the numbers make sense). Also only respond with the CSV.
"""

# Generate synthetic data
response = client.chat.completions.create(
    model=datagen_model,
    messages=[
        {"role": "system", "content": "You are a helpful assistant designed to generate synthetic data."},
        {"role": "user", "content": question}
    ]
)

# Extract the CSV content from the response
csv_data = response.choices[0].message.content.strip()

# Save the CSV content to a file
output_file = "housing_data.csv"
with open(output_file, "w") as file:
    file.write(csv_data)

print(f"Data successfully saved to {output_file}")
