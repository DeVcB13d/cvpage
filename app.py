from resume_converter import *
from resume_parser_openai import *
import tempfile
import io


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
            parsed_resume_path = resume_convert(uploaded_file_path, f"results/Generated_Resume_{uploaded_file.name}.html",uploaded_file)

            # opening the file 
            
            st.sidebar.write('Template resume downloaded!')
            # json_resume = re.sub(r'[^\x20-\x7E]', '', parsed_resume).replace("\n", "\\n").replace("\t", "\\t").replace("\r", "\\r")
            # # end_time = time.time()
            # # elapsed_time = end_time - start_time
            # # st.write(f"Execution time for {uploaded_file.name}: {elapsed_time:.2f} seconds")
            # json_resume = json.loads(json_resume)
            # json_data=json_resume
            # st.write(json_resume)
            # if json_data is None:
            #     raise ValueError("No data provided to create the document")

            # # Generate and download resumes for each template
            # for template_type, create_func in [("KGP", create_doc_from_json_template1), ("Simple", create_doc_from_json_template2), ("2Column", create_doc_from_json_template3)]:
            #     st.write('Creating doc:')
            #     st.write(template_type)
            #     doc_filename = f"Generated_Resume_{template_type}_{uploaded_file.name}.docx"
            #     doc_bytes = create_func(json_resume, doc_filename)
            #     download_docx(doc_bytes, doc_filename)