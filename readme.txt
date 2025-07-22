Introduction
The goal of this project is to develop an automated receipt and bill processing system that extracts structured data such as vendor name, date, amount, and category from varied receipt formats. This tool simplifies financial record-keeping and spending analysis by converting physical or digital receipts into searchable, analyzable data. It is particularly useful for individuals and businesses looking to automate expense tracking and generate summarized insights like total spend, top vendors, and monthly billing trends.

Setup Steps

1. Clone the project repository to your local machine.

2. Create and activate a Python virtual environment to isolate dependencies.

3. Install required packages using pip install -r requirements.txt.

4. Ensure Tesseract OCR is installed and properly configured on your system. (For Windows, make sure the Tesseract executable path is added to the environment variables or specified explicitly in the code.)

5. Run the backend API server using Uvicorn with the command uvicorn main:app --reload.

6. Optionally, run the frontend Streamlit app if included, which connects to the backend APIs.

Design Choices and Architecture

1. The project uses a modular architecture separating concerns clearly: the FastAPI backend handles API routes and server logic; parser.py contains OCR and rule-based parsing logic; db.py manages database interactions; analytics.py computes spending statistics; and schemas.py defines data models.

2. Rule-based parsing was chosen for extracting structured data from OCR text because it allows explicit control over how variable receipt formats are handled without relying on complex, hard-to-tune AI models. This ensures transparent, debuggable, and deterministic extraction capabilities aligned with assignment requirements.

3. The backend stores parsed data in a SQLite database and provides endpoints for uploading receipts, querying stored data with search and filters, and viewing various analytics like monthly spend and vendor frequency.

4. These design choices emphasize clarity, maintainability, and adherence to project specifications emphasizing rule-based or OCR-driven extraction.

Limitations and Assumptions

1. Receipt formats are highly variable; some layouts present challenges for rule-based parsing, leading to missed or incorrect attribute extraction.

2. OCR accuracy depends on image quality; blurred or skewed images might yield noisy or incomplete text, affecting parsing outcomes.

3. Dates and amounts can appear in diverse formats and positions, so regex and keyword approaches sometimes fail or require manual correction.

4. The system assumes receipts use supported formats (PNG, JPG, PDF, TXT) and reasonable English-language text; exotic languages or heavy graphical content may reduce accuracy.

Future Enhancements

1. Integrating large language models such as Google’s Gemini API with prompt engineering can significantly improve parsing accuracy by understanding context, formatting, and semantic meaning in receipts beyond fixed keyword patterns.

2. Machine learning models trained specifically on receipt datasets (e.g., LayoutLM or Donut) can automate structural understanding and field extraction with higher robustness to varied layouts and noisy OCR results.

3. Adding an interactive frontend for manual verification and correction of parsed fields can enhance data quality and user experience.

4. Expanding analytics capabilities with category prediction, anomaly detection, and predictive budgeting would increase the system’s utility for end users.
