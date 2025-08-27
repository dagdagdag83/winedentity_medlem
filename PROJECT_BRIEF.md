## **Project Prompt: Winedentity Membership Registration App**

### **1. Project Overview** 📜

Build a simple Python Flask web application for "Foreningen Winedentity" to handle new membership registrations. The site will feature a single form. Upon submission, the backend will validate the data, save it to a **Firebase Firestore** database which will act as the official **membership register** ("medlemsregister"), and then display a confirmation page with a unique **membership number** ("medlemsnummer").

***

### **2. Tech Stack** 💻

* **Backend:** Python 3.13, Flask
* **Forms:** Flask-WTF for form creation and validation.
* **Frontend:** Jinja2 for HTML templating, styled with **Bootstrap 5**.
* **Database:** Google Firebase Firestore.

***

### **3. Core Features & User Flow** ➡️

1.  **Display Form:** The main page (`/`) will display the membership registration form. The HTML template for the form must use **Bootstrap 5** for layout and styling.
2.  **Submission & Validation:**
    * On form submission (`POST` request), the Flask backend uses Flask-WTF to validate the input.
    * If validation fails, the form should be re-displayed with clear, Bootstrap-styled error messages.
3.  **Data Processing & Storage:**
    * If validation succeeds, the backend connects to Firestore.
    * It generates a **new, unique, sequential membership number**. For example, if the last member was #1023, the new one should be #1024.
    * It saves the member's data from the form, the new membership number, and a `registration_date` timestamp as a new document in the `members` collection.
4.  **Confirmation:**
    * After the data is saved successfully, the user is redirected to a success page (e.g., `/success`).
    * This page must clearly display the user's generated **membership number** and a message instructing them to use it as a reference when paying the membership fee.

***

### **4. Form & Data Model (Placeholder)** 📝

The exact form fields and the final Firestore data model will be provided later.

For now, please implement a **dummy model** to build the application's core logic. The placeholder form should include at least a `full_name` (Text, Required) and `email` (Email, Required) field to ensure the end-to-end flow can be tested.

***

### **5. Deployment** 🚀

* **Platform:** The application must be containerized using a `Dockerfile` for deployment to **Google Cloud Run**.
* **CI/CD:** Create a **GitHub Actions** workflow (`.github/workflows/deploy.yml`) that automatically builds and deploys the application.
* **Workflow Trigger:** The action should trigger on every push to the `main` branch.
* **Workflow Steps:** The workflow must:
    1.  Build the Docker image.
    2.  Push the image to Google Artifact Registry.
    3.  Deploy the new image to the Google Cloud Run service.