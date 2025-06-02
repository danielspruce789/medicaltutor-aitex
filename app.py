from flask import Flask, render_template, request, session, jsonify
from pypdf import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.llms import HuggingFaceHub
from langchain import PromptTemplate
import os
import tempfile
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "med_study_assistant_secret_key"  # Change this in production

# Template for custom prompt
template = """ 
You are a tutor helping me study for my medical exam using the provided context. 
{query}
"""

# Initialize the prompt
prompt = PromptTemplate.from_template(template)

def get_vectors(chunks):
    """
    Computes the embeddings using pubmedbert-base-embeddings,
    uses FAISS to store them.
    """
    embeddings = HuggingFaceEmbeddings(model_name="NeuML/pubmedbert-base-embeddings")
    vectorstore = FAISS.from_texts(texts=chunks, embedding=embeddings)
    return vectorstore

def get_pdf_text(file_path):
    """Reads a pdf document and returns all of it as a string"""
    text = ""
    pdf_reader = PdfReader(file_path)
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def get_chunks(text):
    """Splits the text into chunks"""
    text_splitter = CharacterTextSplitter(
        separator="\n", chunk_size=1000, chunk_overlap=200, length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks

def get_conv(vects):
    """Creating a conversation chain"""
    llm = HuggingFaceHub(
        repo_id="mistralai/Mixtral-8x7B-Instruct-v0.1",
        model_kwargs={"temperature": 0.0, "max_length": 2048},
    )
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm, retriever=vects.as_retriever(), memory=memory
    )
    return conversation_chain

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'document' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['document']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and file.filename.endswith('.pdf'):
        # Create a temporary file to save the PDF
        temp_dir = tempfile.gettempdir()
        filename = secure_filename(file.filename)
        filepath = os.path.join(temp_dir, filename)
        file.save(filepath)
        
        # Process the PDF file
        try:
            raw_text = get_pdf_text(filepath)
            chunks = get_chunks(raw_text)
            vects = get_vectors(chunks)
            
            # Store in session
            session['vectorstore'] = vects
            session['chat_history'] = []
            
            # Create conversation
            conversation = get_conv(vects)
            # We'll store this in some session data (Note: this is a simplified example)
            session['conversation_ready'] = True
            
            return jsonify({'success': 'File processed successfully!'}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        finally:
            # Clean up the temporary file
            if os.path.exists(filepath):
                os.remove(filepath)
    else:
        return jsonify({'error': 'Only PDF files are supported'}), 400

@app.route('/query', methods=['POST'])
def process_query():
    if not session.get('conversation_ready'):
        return jsonify({'error': 'Please upload and process a document first'}), 400
    
    data = request.json
    query = data.get('query')
    
    if not query:
        return jsonify({'error': 'No query provided'}), 400
    
    try:
        # Format the query with the prompt
        question = str(prompt.format(query=query))
        
        # Get the conversation chain
        vects = session.get('vectorstore')
        conversation = get_conv(vects)
        
        # Get response
        response = conversation({"question": question})
        chat_history = response["chat_history"]
        
        # Update session
        session['chat_history'] = chat_history
        
        # Extract the last bot message
        bot_response = chat_history[-1].content
        
        return jsonify({
            'user_message': query,
            'bot_response': bot_response
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)