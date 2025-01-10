import pdfplumber
import re
from transformers import AutoTokenizer, AutoModelForCausalLM

# Step 1: Extract text from PDFs
def extract_text_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text

# Load the PDFs
motor_vehicle_text = extract_text_from_pdf("check_list_of__documents__for_motor_vehicle_registration.pdf")
cnic_text = extract_text_from_pdf("check_list_of__documents__for_new_cnic.pdf")
domicile_text = extract_text_from_pdf("check_list_of__documents__for_domicile.pdf")

# Step 2: Extract checklists using regex
def extract_checklist(text):
    checklist = re.findall(r'\d+\.\s(.+)', text)
    return checklist

motor_vehicle_checklist = extract_checklist(motor_vehicle_text)
cnic_checklist = extract_checklist(cnic_text)
domicile_checklist = extract_checklist(domicile_text)

# # Display extracted checklists for debugging
# print("Motor Vehicle Checklist:", motor_vehicle_checklist)
# print("CNIC Checklist:", cnic_checklist)
# print("Domicile Checklist:", domicile_checklist)

# Step 3: Few-shot prompting examples
few_shot_examples = """
Objective: Identify and extract key items or prerequisites from checklists.

Example:
Input: What are the requirements for a new CNIC?
Output: Checklist: 1) Birth Certificate, 2) Matriculation Certificate, 3) CNIC of immediate relatives, 4) Citizenship certificate by MOI.

Input: What documents are needed for motor vehicle registration?
Output: Checklist: 1) Application Form-F, 2) Valid CNIC, 3) Sales Invoice, 4) Sales Certificate, 5) Proof of payment for taxes.

"""

# Step 4: Load the model and tokenizer
tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-3.2-1B")
model = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-3.2-1B")

# Function to query the model
def query_model(query):
    input_text = few_shot_examples + f"Input: {query}\nOutput:"
    inputs = tokenizer.encode(input_text, return_tensors="pt")
    outputs = model.generate(
        inputs,
        max_length=300,
        num_return_sequences=1,
        temperature=0.7,
        top_p=0.9,
        pad_token_id=tokenizer.eos_token_id,
    )
    return tokenizer.decode(outputs[0], skip_special_tokens=True).split("Output:")[-1].strip()

# Step 5: Test the model with a query
query = "What are the requirements for motor vehicle registration?"
response = query_model(query)
print("Response:", response)
