import subprocess
import os
from PyPDF2 import PdfReader

def run_ollama(prompt):
    # Run Ollama with the model name and the crafted prompt
    result = subprocess.run(
        ['ollama', 'run', 'llama3.2:latest', prompt],
        capture_output=True,
        text=True
    )
    
    # Check for errors and print the output
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
        return None
    else:
        return result.stdout.strip()

# Function to extract text from PDFs
def extract_text_from_pdfs(directory):
    texts = {}
    for filename in os.listdir(directory):
        if filename.endswith(".pdf"):
            filepath = os.path.join(directory, filename)
            reader = PdfReader(filepath)
            text = "".join(page.extract_text() for page in reader.pages)
            texts[filename] = text
    return texts

# Function to generate a prompt for extracting checklist items
def generate_prompt_for_checklist_extraction(document_text, form_name="Bayform"):
    prompt = f"""
    Task: Extract the checklist items or requirements for the following form: {form_name}.
    
    Example 1:
    Document: "For the domicile application form, the applicant must provide: Name, CNIC Number, Date of Birth, Address, and Proof of Residence."
    Checklist Items: Name, CNIC Number, Date of Birth, Address, Proof of Residence.

    Example 2:
    Document: "For the driving license form, mandatory fields include: Applicant's Name, CNIC Number, Address, and Driving Test Date."
    Checklist Items: Applicant's Name, CNIC Number, Address, Driving Test Date.

    Document Text: {document_text}

    Checklist Items or Prerequisites for {form_name}:
    """
    return prompt

# Function to process documents and respond to user queries
def process_documents_for_checklist(directory, form_name="birth-certificate-form-b"):
    documents = extract_text_from_pdfs(directory)
    form_text = documents.get(f"{form_name}.pdf", None)  # Retrieve the specific form text
    if form_text:
        prompt = generate_prompt_for_checklist_extraction(form_text, form_name)
        response = run_ollama(prompt)
        if response:
            print(f"Checklist Items or Prerequisites for {form_name}: {response}\n")
        else:
            print(f"Could not extract checklist items for {form_name}.")
    else:
        print(f"{form_name}.pdf not found in the directory.")

# Allow the user to query for the requirements of a specific form
def query_form_requirements(directory):
    while True:
        # Ask the user for the form name (e.g., Bayform, Domicile, etc.)
        form_name = input("Enter the form name (e.g., Bayform, Domicile, Driving License) or type 'exit' to quit: ")
        if form_name.lower() == 'exit':
            break

        # Process the form and extract the checklist
        process_documents_for_checklist(directory, form_name)

# Directory containing the PDF documents
document_directory = "/home/cs/internship/Punjab_ekhidmat_Markaz"  # Replace with your directory

# Allow the user to interact and ask questions about the checklist of the forms
query_form_requirements(document_directory)
