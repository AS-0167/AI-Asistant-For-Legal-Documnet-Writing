from transformers import AutoTokenizer, AutoModelForCausalLM
from fpdf import FPDF
import os

# Load the model and tokenizer from Hugging Face
tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-3.2-1B")
model = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-3.2-1B")

# Function to generate text using the LLaMA model
def generate_certificate_with_transformers(prompt, max_length=1024):
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

# Function to save the birth certificate as a PDF
def save_certificate_to_pdf(content, output_pdf_path):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, content)
    pdf.output(output_pdf_path)
    print(f"Birth certificate saved as {output_pdf_path}")

# Function to load the prompt template
def load_prompt_template(template_path):
    with open(template_path, "r") as file:
        return file.read()

# Main function
def main():
    input_file_path = "birth_certificate_info.txt"
    template_file_path = "birth.txt"
    output_pdf_path = "birth_certificate.pdf"

    # Check if user info exists
    if os.path.exists(input_file_path):
        with open(input_file_path, "r") as file:
            user_info = {line.split(": ")[0]: line.split(": ")[1].strip() for line in file.readlines()}
    else:
        # Get user input
        user_info = {}
        print("Please provide the following information:")
        user_info["Applicant Name"] = input("Applicant Name: ")
        user_info["Applicant CNIC No."] = input("Applicant CNIC No.: ")
        user_info["Child Name"] = input("Child Name: ")
        user_info["Relation"] = input("Relation to Child: ")
        user_info["Gender"] = input("Gender (Male/Female): ")
        user_info["Religion"] = input("Religion: ")
        user_info["Father's Name"] = input("Father's Name: ")
        user_info["Father's CNIC No."] = input("Father's CNIC No.: ")
        user_info["Mother's Name"] = input("Mother's Name: ")
        user_info["Mother's CNIC No."] = input("Mother's CNIC No.: ")
        user_info["Grandfather's Name"] = input("Grandfather's Name: ")
        user_info["Grandfather's CNIC No."] = input("Grandfather's CNIC No.: ")
        user_info["District of Birth"] = input("District of Birth: ")
        user_info["Father's Occupation"] = input("Father's Occupation: ")
        user_info["Vaccinated"] = input("Vaccinated (Yes/No): ")
        user_info["Disability"] = input("Disability (Yes/No): ")
        user_info["Address"] = input("Address: ")
        user_info["Date of Birth"] = input("Date of Birth: ")
        user_info["Place of Birth"] = input("Place of Birth (Home/Hospital/Health Center): ")
        user_info["Date of Registration"] = input("Date of Registration: ")
        user_info["Mobile Number"] = input("Mobile Number: ")

        # Save input to a text file
        with open(input_file_path, "w") as file:
            for key, value in user_info.items():
                file.write(f"{key}: {value}\n")

    # Load the prompt template
    prompt_template = load_prompt_template(template_file_path)

    # Fill the template with user input
    filled_prompt = prompt_template
    for key, value in user_info.items():
        filled_prompt = filled_prompt.replace(f"{{{{{key}}}}}", value)

    # Generate the birth certificate using the LLaMA model
    certificate_content = generate_certificate_with_transformers(filled_prompt)

    # Save the generated certificate to a PDF
    save_certificate_to_pdf(certificate_content, output_pdf_path)

if __name__ == "__main__":
    main()
