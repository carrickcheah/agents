from openai import OpenAI
import json
from loguru import logger

# Initialize OpenAI client
client = OpenAI()

# Model for data generation
datagen_model = "gpt-4o-mini"

# Template for Q&A sets in JSONL format
def generate_jsonl_entry(question, answer):
    return {
        "messages": [
            {"role": "system", "content": "You are a helpful assistant to assist customers in the hotel business."},
            {"role": "user", "content": question},
            {"role": "assistant", "content": answer}
        ]
    }

# Question to generate data
question = """
Create 15 rows of Q&A data for the hotel business. Each row should include:

- A frequently asked question related to the hotel business, such as booking, facilities, check-in policies, etc.
- A detailed and professional response to the corresponding question.

Ensure the Q&A pairs are relevant to hotel operations and customer interactions. Include common topics like reservations, amenities, cancellation policies, local attractions, and customer service. Only respond with pairs of question and answer.
"""

# Generate synthetic data with progress tracking
logger.info("Starting data generation...")
response = client.chat.completions.create(
    model=datagen_model,
    messages=[
        {"role": "system", "content": "You are a helpful assistant designed to generate synthetic data."},
        {"role": "user", "content": question}
    ]
)

logger.info("Data generation in progress...")

# Extract generated Q&A content
qa_data = response.choices[0].message.content.strip()
qa_rows = qa_data.split("\n")  # Split into rows

logger.info("Data extraction complete. Preparing JSONL entries...")

# Prepare JSONL entries
output_file = "hotel_qa_data.jsonl"
with open(output_file, "w") as file:
    buffer_question = None
    for idx, row in enumerate(qa_rows):
        row = row.strip()
        if row.startswith("**Question:**"):
            buffer_question = row.replace("**Question:**", "").strip()
        elif row.startswith("**Answer:**") and buffer_question:
            answer = row.replace("**Answer:**", "").strip()
            jsonl_entry = generate_jsonl_entry(buffer_question, answer)
            file.write(json.dumps(jsonl_entry) + "\n")
            logger.info(f"Processed entry {idx + 1}")
            buffer_question = None  # Reset for the next question
        elif not row:  # Skip blank lines
            continue
        else:
            logger.warning(f"Skipping malformed row {idx + 1}: {row}")

logger.success(f"Data successfully saved to {output_file}")
