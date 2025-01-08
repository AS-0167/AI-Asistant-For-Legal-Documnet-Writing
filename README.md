# Legal Document Assistant

## 🚀 Overview

The **Legal Document Assistant** is an AI-powered web application designed to assist users in writing legal documents effortlessly and securely. This application simplifies the process of drafting legal documents by automating the retrieval of relevant information, integrating user data, and leveraging advanced AI technologies. It is tailored to work with the legal framework of the **Government of Punjab, Pakistan** and offers features such as data scraping, fine-tuning, and a secure data storage mechanism.

---

## ✨ Key Features

### 1. **AI-Assisted Legal Document Writing**
- Automates the creation of legal documents such as affidavits, power of attorney, contracts, and agreements.
- Uses **few-shot prompting** to provide accurate, high-quality document drafting.
- Customizes the documents based on the user's selected type and inputs.

### 2. **Legal Data Scraping**
- Scrapes data from verified government websites to stay up-to-date with legal terminologies and templates.
- Fine-tunes the AI model with the latest legal data for enhanced accuracy.

### 3. **Secure User Data Storage**
- Personal information (e.g., full name, father's name, CNIC, address, gender, marital status) is stored locally on the user's machine in an encrypted format.
- Only the combination of the username and password can be used as the decryption key, ensuring robust security.

### 4. **Local Server Deployment**
- The application runs entirely on a **local server** to keep user data private and separate.
- No reliance on external APIs for AI processing, ensuring complete control over data and privacy.

---

## 🛠️ How It Works

### 1. **User Input**
- The user selects the type of legal document to draft and provides their username and password.
- The application fetches and decrypts the user's securely stored data to fill in the necessary fields.

### 2. **Data Scraping and AI Fine-Tuning**
- Legal data is scraped from government websites and integrated into the AI model for fine-tuning.
- The application ensures that document templates and terminologies are consistent with the **Government of Punjab, Pakistan**.

### 3. **Document Drafting**
- The AI assistant generates the requested document with prefilled data and user-specific customizations.
- Users can review, edit, and finalize the document.

---

## 📄 Legal Documents Supported
This application supports the drafting of various legal documents, including but not limited to:
- Affidavits
- Contracts
- Agreements
- Power of Attorney
- Nikkah Nama (Marriage Contract)
- Sale Deeds
- Rental Agreements
- Will and Testament
- Divorce Deeds

---

## ⚙️ Technology Stack

### **1. Language Model**
- **LLama 3.2 (7B)**: The Large Language Model (LLM) used for document drafting is fine-tuned on local legal data and runs on a **local server** for security.

### **2. Data Encryption**
- User data is stored locally in an encrypted format.
- A hybrid key is generated using the username and password for decryption.

### **3. Backend**
- **Python**, with **Hugging Face Transformers** for model integration.
- Fine-tuning and few-shot prompting enhance document accuracy.

### **4. Frontend**
- **will decide later**: Provides a user-friendly interface for document selection and data input.

---

## 🖥️ Security and Privacy
- **Local Server**: The application does not use external APIs, ensuring all operations are performed locally.
- **Data Encryption**: User data is encrypted on the local machine and can only be accessed with the correct username and password combination.
- **No Third-Party Data Sharing**: All user data and operations are kept private and secure.

---

## 🔄 Installation and Usage

### Prerequisites
- Python 3.8+
- Hugging Face Transformers
- Streamlit
- Pandas
- PyCryptodome (for encryption)

### Steps to Install
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/legal-document-assistant.git
   ```
2. Navigate to the project directory:
   ```bash
   cd legal-document-assistant
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the application:
   ```bash
   streamlit run app.py
   ```

---

## 💪 Future Enhancements
- **Multi-Language Support**: Expand support for additional languages and legal systems.
- **Additional Document Types**: Add more templates based on user feedback.
- **Cloud Integration**: Optional secure cloud backup for user data.

---

## 🛡️ Disclaimer
This application is designed for educational and practical purposes and is tailored for the **Government of Punjab, Pakistan**. Users are advised to consult legal professionals for complex legal matters.

Enjoy drafting legal documents with ease and security!
