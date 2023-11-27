'''
Module for testing the app.py file without running the openai api
'''
sample_parsed_resume = './parsed_resume.txt'

from resume_converter import *
from resume_parser_openai import *
import tempfile


# Streamlit UI
st.title('Resume Parser and Builder')

uploaded_files = st.file_uploader("Upload your resumes here", type=["pdf", "doc", "docx", "txt"], accept_multiple_files=True)
        
if st.button('Create Resumes') and uploaded_files:
    for uploaded_file in uploaded_files:
        temp_dir = tempfile.mkdtemp()
        uploaded_file_path = os.path.join(temp_dir, uploaded_file.name)
        with open(uploaded_file_path, "wb") as f:
                f.write(uploaded_file.getvalue())
            
        # resume_text = convert_files_to_text(uploaded_file_path)
        # resume_text = truncate_text_by_words(resume_text)
        st.write('We have the text! Yaaaaaayyyyyyyy')
        
        with st.spinner(f'Parsing resume: {uploaded_file.name}...'):
            # start_time = time.time()
            st.write('Here we go, start parsing!')
            # json_resume = run_async_code(systems, resume_text)
            # parsed_resume = parse_resume(resume_text)
            parsed_resume = resume_convert(uploaded_file_path, f"results/Generated_Resume_{uploaded_file.name}.html",uploaded_file)
            
            st.sidebar.write('Resume parsed!')