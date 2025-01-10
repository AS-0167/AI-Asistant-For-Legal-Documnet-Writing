from transformers import AutoModelForCausalLM, AutoTokenizer

interships = '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'
internhip2 = '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'

model_name = "tiiuae/falcon-7b" 
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

input_text = "Write a legal document template for a rental agreement."
inputs = tokenizer(input_text, return_tensors="pt")
outputs = model.generate(**inputs)
print(tokenizer.decode(outputs[0]))
