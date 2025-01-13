from transformers import AutoTokenizer, AutoModelForCausalLM
from fpdf import FPDF
import os

# Load the model and tokenizer from Hugging Face
tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-3.2-1B")
model = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-3.2-1B")

# Function to generate text using the LLaMA model
def generate_affidavit_with_transformers(prompt, max_length=500):
    inputs = tokenizer(prompt, return_tensors="pt")
    outputs = model.generate(
        **inputs,
        max_length=max_length,
        temperature=0.7,  # Adjust for more/less creativity
        top_p=0.9,       # Nucleus sampling
        num_return_sequences=1
    )
    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return generated_text

# Function to save the affidavit as a PDF
def save_affidavit_to_pdf(content, output_pdf_path):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, content)
    pdf.output(output_pdf_path)
    print(f"Affidavit saved as {output_pdf_path}")

# Main function
def main():
    text_file_path = "form.txt"
    prompt_file_path = "prompt.txt"  # The text file containing the prompt template
    output_pdf_path = "affidavit_transformers.pdf"

    # Check if user info exists
    if os.path.exists(text_file_path):
        with open(text_file_path, "r") as file:
            user_info = {line.split(": ")[0]: line.split(": ")[1].strip() for line in file.readlines()}
    else:
        # Get user input
        user_info = {}
        print("Please provide the following information:")
        user_info["name"] = input("Full Name: ")
        user_info["father_name"] = input("Father's Name: ")
        user_info["address"] = input("Address: ")
        user_info["residence_since"] = input("Residing in Rawalpindi since (Year): ")
        user_info["nic"] = input("NIC Number: ")

        # Save input to a text file
        with open(text_file_path, "w") as file:
            for key, value in user_info.items():
                file.write(f"{key}: {value}\n")

    # Read the prompt from the text file
    if os.path.exists(prompt_file_path):
        with open(prompt_file_path, "r") as file:
            prompt_template = file.read()
    else:
        print(f"Prompt file '{prompt_file_path}' not found!")
        return

    # Format the prompt with user information
    prompt = prompt_template.format(
        name=user_info['name'],
        father_name=user_info['father_name'],
        address=user_info['address'],
        residence_since=user_info['residence_since'],
        nic=user_info['nic']
    )
    
    # Generate the affidavit using the LLaMA model
    affidavit_content = generate_affidavit_with_transformers(prompt)

    # Save the generated affidavit to a PDF
    save_affidavit_to_pdf(affidavit_content, output_pdf_path)

if __name__ == "__main__":
    main()
