'''
Module to process the user resume and return the following fields:

TODO FIELDS:

1. Name [x]
2. Email [x]
3. Phone [x]
4. Position/Designation [x]
5. About Me []
6. Work Experience []
7. Education [x]
8. Expertise/Skills [x]
9. Language []
10. References []
11. Picture [x]
12. Address [x]
13. Social Media Links [x]

'''


from resume_parser import resumeparse
import os
import pandas as pd
import spacy
import re
import spacy
import nltk
from nltk.corpus import stopwords
import fitz 
import io 
from PIL import Image 
from spacy.matcher import Matcher
from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
import io


spacy.cli.download('en_core_web_sm')
nltk.download('stopwords')
# load pre-trained model
nlp = spacy.load('en_core_web_sm')

# Grad all general stop words
STOPWORDS = set(stopwords.words('english'))

'''
Python code to process the resumes and return the following fields


input: resume file path
'''

def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as fh:
        # iterate over all pages of PDF document
        for page in PDFPage.get_pages(fh, caching=True, check_extractable=True):
            # creating a resoure manager
            resource_manager = PDFResourceManager()
            
            # create a file handle
            fake_file_handle = io.StringIO()
            
            # creating a text converter object
            converter = TextConverter(
                                resource_manager, 
                                fake_file_handle, 
                                codec='utf-8', 
                                laparams=LAParams()
                        )

            # creating a page interpreter
            page_interpreter = PDFPageInterpreter(
                                resource_manager, 
                                converter
                            )

            # process current page
            page_interpreter.process_page(page)
            
            # extract text
            text = fake_file_handle.getvalue()
            yield text

            # close open handles
            converter.close()
            fake_file_handle.close()
        
def process(file):
    resume_text = ''
    # Getting resumetext to process skills
    for page in extract_text_from_pdf(file):
        resume_text += ' ' + page
    # Resume text to process 
    datatxt = resumeparse.read_file(file)
    print(datatxt)
    extract = {}
    extract["name"] = extract_name(resume_text)
    extract["email"] = datatxt["email"]
    extract["phone"] = datatxt["phone"]
    extract["designition"] = datatxt["designition"]
    extract["skills"] = process_skills(resume_text)
    extract["education"] = extract_education(resume_text)
    extract["photo_path"] = extract_photo(file)
    extract["experience"] = extract_experience(resume_text)
    extract["links"] = extract_links(resume_text)
    extract["address"] = extract_address(resume_text)
    extract["about"] = extract_about(resume_text)

    return extract

'''
The following function extracts the name from the resume text
A name is mostly 2-3 Proper Nouns, so we use a matcher to match the pattern
'''
def extract_name(resume_text):

    # Matcher class object
    matcher = Matcher(nlp.vocab)

    # Processing the text into a spaCy Doc object
    nlp_text = nlp(resume_text)
    
    # First name and Last name are mostly Proper Nouns
    pattern1 = [{'POS': 'PROPN'}, {'POS': 'PROPN'}]
    pattern2 = [{'POS': 'PROPN'}, {'POS': 'PROPN'}, {'POS': 'PROPN'}]
    
    # Add the pattern to the matcher
    matcher.add('NAME', [pattern1, pattern2])
    
    matches = matcher(nlp_text)
    
    for match_id, start, end in matches:
        span = nlp_text[start:end]
        return span.text
    
'''
The following function extracts the links from the resume text
It uses a regex to match the pattern of a link
'''
def extract_links(resume_text):
    # Regex to find a URL
    link_regex = r'https?://(?:www\.)?[a-zA-Z0-9-]+\.[a-zA-Z]{2,}(?:/[a-zA-Z0-9-._%~+]*)*'
    links = re.findall(link_regex, resume_text)
    links = [link.split()[0].strip(';') for link in links]
    if len(links) == 0:
        return None
    return [links[0]]

'''
The following function extracts the address from the resume text
It uses the spacy NER to find the address
Address is mostly a GPE (Geopolitical Entity)
'''
def extract_address(resume_text):
    resume_text = nlp(resume_text)
    for entity in resume_text.ents:
        if entity.label_ == 'GPE':
            return entity.text
    return None

'''
The following function extracts the skills from the resume text
'''
def process_skills(resume_text):
    # load pre-trained model
    nlp = spacy.load('en_core_web_sm')
    
    nlp_text = nlp(resume_text)
    noun_chunks = nlp_text.noun_chunks

    # removing stop words and implementing word tokenization
    tokens = [token.text for token in nlp_text ]
    
    # reading the csv file
    data = pd.read_csv("skills.csv")

    # extract values
    skills = list(data.columns.values)

    skillset = []

    # check for one-grams (example: python)
    for token in tokens:
        if token.lower() in skills:
            skillset.append(token)
    
    # check for bi-grams and tri-grams (example: machine learning)
    for token in noun_chunks:
        token = token.text.lower().strip()
        if token in skills:
            skillset.append(token)
    
    return [i.capitalize() for i in set([i.lower() for i in skillset])]

def extract_education(resume_text):
    EDUCATION = [
            'BE','B.E.', 'B.E', 'BS', 'B.S', 
            'ME', 'M.E', 'M.E.', 'MS', 'M.S', 
            'BTECH', 'B.TECH', 'M.TECH', 'MTECH', 
            'SSC', 'HSC', 'CBSE', 'ICSE', 'X', 'XII','SSLC','SCHOOL'
            'MASTER', 'BACHELOR', 'DEGREE', 'GRADUATION', 'POST GRADUATION', 'UNDER GRADUATION','GRADUATE','POST GRADUATE','UNDER GRADUATE',
            'AISSCE'
        ]
    nlp_text = nlp(resume_text)


    # Sentence Tokenizer
    nlp_text = [sent.string.strip() for sent in nlp_text.sents]

    edu = {}
    # Extract education degree
    for index, text in enumerate(nlp_text):
        for tex in text.split():
            # Replace all special symbols
            tex = re.sub(r'[?|$|.|!|,]', r'', tex)
            if tex.upper() in EDUCATION and tex not in STOPWORDS:
                edu[tex] = text + nlp_text[index + 1]

    # Extract year
    education = []
    for key in edu.keys():
        year = re.search(re.compile(r'(((20|19)(\d{2})))'), edu[key])
        if year:
            education.append((key, ''.join(year[0])))
        else:
            education.append(key)
    return education

def extract_photo(file_path):
    pdf_file = fitz.open(file_path)
    # iterate over PDF pages 
    for page_index in range(len(pdf_file)): 
    
        # get the page itself 
        page = pdf_file[page_index] 
        image_list = page.get_images() 
    
        for image_index, img in enumerate(page.get_images(), start=1): 
    
            # get the XREF of the image 
            xref = img[0] 
    
            # extract the image bytes 
            base_image = pdf_file.extract_image(xref) 
            image_bytes = base_image["image"] 
    
            # get the image extension 
            image_ext = base_image["ext"] 
            
            file_name = os.path.splitext(os.path.basename(file_path))[0]

            name = os.path.splitext(os.path.basename(file_name))[0]
            # load it to PIL
            image = Image.open(io.BytesIO(image_bytes))
            image_path = os.path.join("results/images", "image_"+ name +".png")
            image.save(image_path, image_ext)
            image_load_path = os.path.join("images", "image_"+ name +".png")
            return image_load_path
    return None


'''
Extracting user experience from the resume

The main contents of experience are:
1. Company Name
2. Position
3. Duration
4. Description

TODO: Extract the above fields from the resume

Currently, the following fields are hardcoded

return: dictionary of experience

'''
def extract_experience(resume_text):
    exp = {}
    exp['job_titles'] = ['AI ML Engineer', 'Data Scientist', 'Software Engineer', 'Flutter Developer', 'Full Stack Developer']
    exp['job_companies'] = ['PIXEL PVT','KIT Tech','Aloop Inc','Firebase media','LSI gen']
    exp['job_dates'] = ['2018-2020','2019-2020','2019-2020','2019-2020','2019-2020']
    exp['job_descriptions'] = [
        'Worked on AI based projects and developed a deep learning model for detecting and classifying objects in images',
        'Worked on various projects related to computer vision and deep learning',
        'Worked on various projects related to data science and machine learning',
        'Worked on various projects related to flutter development',
        'Worked on various projects related to full stack development'
    ]
    return exp

'''
Extracting user about from the resume

TODO: Extract the about field from the resume
Currently, the following fields are hardcoded
'''
def extract_about(resume_text):
    return '''I am a passionate AI & ML enthusiast with experience in various technology stacks and libraries,
        specializing in projects related to computer vision and deep learning. I am also skilled in Flutter development. I am currently pursuing an Integrated MSc in Computer Science with a specialization in AI & Data
        Science
        '''


    

def test():
    resumes_dir = "./data"
    for res in os.listdir(resumes_dir):
        print("Processing {0}".format(res))
        data = process(os.path.join(resumes_dir,res))
        print(data)

if __name__ == "__main__":
    test()

