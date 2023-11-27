'''
Pipeline to run the resume conversion app
'''

from resume_parser_spacy import process
from html_convert import fill_resume_template
from resume_parser_openai import convert_files_to_text, parse_resume, truncate_text_by_words
import pdfkit
import json
import os
'''
Preprocess the data from the processed user data to make
it compatible with the HTML template


'''


# Combine the data from the two parsers
def combine_data(parsed_resume_0, parsed_resume_openai):
    print(parsed_resume_openai)
        
    data = {}
    data["name"] = parsed_resume_openai["name"]
    data["gmail"] = parsed_resume_openai["gmail"]
    data["phone number"] = parsed_resume_openai["phone number"]
    data["skillset and expertise"] = parsed_resume_openai["skillset and expertise"]
    data["education"] = parsed_resume_0["education"]
    data["photo_path"] = parsed_resume_0["photo_path"]
    # Need to change this to openai parser
    data["designition"] = parsed_resume_0["designition"]
    data["address"] = parsed_resume_0["address"]
    data["links"] = parsed_resume_0["links"]
    data["Explanation of projects"] = parsed_resume_openai["Explanation of projects"]
    # Need to change this to openai parser
    data["experience"] = parsed_resume_openai["Explanation of projects"] 
    if parsed_resume_openai['Explanation of position of responsibilities'] != None:
        data["experience"]+=parsed_resume_openai['Explanation of position of responsibilities'] 
    
    return data

def preprocess_data(data):
    html_input = {
        "{NAME}": data["name"],
        "{EMAIL}": data["gmail"],
        "{PHONE}": data["phone number"],
        "{SKILLS}": data["skillset and expertise"],
        "{EDUCATION}": data["education"],
        "{IMAGE}": data["photo_path"],
        "{DESIGNATION}": data["designition"],
        "{ADDRESS}": data["address"],
        "{LINKS}": data["links"],
        "{ABOUT}": data["Explanation of projects"][0],
        "{EXPERIENCE}": data["experience"]
    }
    return html_input

def resume_convert(input_resume_path, output_resume_path, input_resume=None):

    # Process the input resume
    # This partially does the parsing by using the resume parser library
    parsed_resume_0 = process(input_resume_path)
    # Convert to text
    resume_text = convert_files_to_text(input_resume)
    resume_text = truncate_text_by_words(resume_text)
    # Load the text in json
    
    # Parse the resume
    # The line below is to debug without calling the openai API
    # parsed_resume_openai = open("parsed_resume.txt", "r").read()
    parsed_resume_openai = parse_resume(resume_text)
    parsed_resume_openai = json.loads(parsed_resume_openai)
    # Combine the data from the two parsers
    data = combine_data(parsed_resume_0, parsed_resume_openai)

    # Preprocess the data
    data = preprocess_data(data)


    print(data)

    # Path to the resume template
    template_path = "./standard/standard.html"

    # Fill the resume template with the data
    fill_resume_template(template_path, output_resume_path, data)


    output_pdf_path = output_resume_path.replace("html", "pdf")

    pdfkit.from_file(output_resume_path, output_pdf_path, verbose=True, options={"enable-local-file-access": True})

    return parsed_resume_openai


def test():
    resumes_dir = "./data"
    for res in os.listdir(resumes_dir):
        name = os.path.splitext(res)[0]
        print("Converting {0} to {1}.html".format(res, name))
        resume_convert(os.path.join(resumes_dir,res), "results/{0}.html".format(name))


if __name__ == "__main__":
    test()