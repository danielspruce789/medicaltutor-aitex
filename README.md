# MedStudy Assistant
## Problem Statement
Medical students face significant challenges in their educational journey due to the vast and complex nature of medical curriculum. Traditional study methods often fail to provide personalized guidance tailored to individual learning needs, making it difficult for students to effectively prepare for their exams. With increasing enrollment in medical schools globally, there is a growing demand for innovative solutions that can enhance the efficiency and effectiveness of medical exam preparation.
## Solution
'MedStudy Assistant' addresses these challenges by offering a personalized approach to medical exam preparation. This application leverages advanced natural language processing technology to analyze your own course materials and provide tailored learning experiences.
## Impact
MedStudy Assistant has the potential to significantly transform medical education by providing:
- Personalized study assistance based on your own materials
- Efficient exam preparation through targeted questions
- Enhanced comprehension of complex medical concepts
- A more accessible approach to medical education globally
## Key Features
Current features:
1. **Document Analysis:** Upload and analyze your own medical course materials
2. **Customized Question Generation:** Generate personalized study questions based on the content of your uploaded documents
Planned features:
3. **Adaptive Learning:**
   - Dynamic question difficulty based on performance
   - Targeted practice for weak areas
   
4. **Feedback and Insights:**
   - Detailed feedback on responses
   - Performance analytics and progress tracking
   
5. **Resource Integration:**
   - Support for various file formats
   - Multi-course support for comprehensive exam preparation

## Architecture
The application follows a client-server architecture:
1. **Frontend**: HTML, CSS, and JavaScript for the user interface
2. **Backend**: Flask web server
3. **PDF Processing**: Extract text from uploaded PDF documents
4. **Text Processing**: Split text into manageable chunks
5. **Embedding Generation**: Generate embeddings using medical-specific model
6. **Vector Database**: Store and query text embeddings using FAISS
7. **LLM Integration**: Generate responses using Mixtral 8x7B
## Installation and Setup
To run MedStudy Assistant locally:
1. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
2. Run the Flask application:
   ```
   python app.py
   ```
## Demo
Check out our application demo:
- [MedStudy_Demo.mp4](medicaltutor_Demo.mp4)
## Usage
1. Upload your medical PDF document using the sidebar
2. Click "Process" to analyze the document
3. Ask questions in the main chat area
4. Receive personalized responses based on your document content