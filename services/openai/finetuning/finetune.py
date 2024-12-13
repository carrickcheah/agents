# %%
import json
import openai
import os
import pandas as pd
from pprint import pprint


# %%
client = openai.OpenAI(
    project=20241213
)

recipe_df = pd.read_csv("/mnt/c/Users/roy12/src/20241212_Stack_agents/services/openai/finetuning/cookbook.csv")

print(recipe_df.head()) 



# %%

system_message = "You are a helpful recipe assistant. You are to extract the generic ingredients from each of the recipes provided."


def create_user_message(row):
    return f"Title: {row['title']}\n\nIngredients: {row['ingredients']}\n\nGeneric ingredients: "


def prepare_example_conversation(row):
    return {
        "messages": [
            {"role": "system", "content": system_message},
            {"role": "user", "content": create_user_message(row)},
            {"role": "assistant", "content": row["NER"]},
        ]
    }


pprint(prepare_example_conversation(recipe_df.iloc[0]))



# use the first 100 rows of the dataset for training
training_df = recipe_df.loc[0:5]

# apply the prepare_example_conversation function to each row of the training_df
training_data = training_df.apply(prepare_example_conversation, axis=1).tolist()

for example in training_data[:5]:
    print(example)

validation_df = recipe_df.loc[101:200]
validation_data = validation_df.apply(
    prepare_example_conversation, axis=1).tolist()

def write_jsonl(data_list: list, filename: str) -> None:
    with open(filename, "w") as out:
        for ddict in data_list:
            jout = json.dumps(ddict) + "\n"
            out.write(jout)


training_file_name = "tmp_recipe_finetune_training.jsonl"
write_jsonl(training_data, training_file_name)

validation_file_name = "tmp_recipe_finetune_validation.jsonl"
write_jsonl(validation_data, validation_file_name)

def upload_file(file_name: str, purpose: str) -> str:
    with open(file_name, "rb") as file_fd:
        response = client.files.create(file=file_fd, purpose=purpose)
    return response.id


training_file_id = upload_file(training_file_name, "fine-tune")
validation_file_id = upload_file(validation_file_name, "fine-tune")

print("Training file ID:", training_file_id)
print("Validation file ID:", validation_file_id)


MODEL = "gpt-4o-mini-2024-07-18"

response = client.fine_tuning.jobs.create(
    training_file=training_file_id,
    validation_file=validation_file_id,
    model=MODEL,
    suffix="recipe-ner",
)

job_id = response.id

print("Job ID:", response.id)
print("Status:", response.status)