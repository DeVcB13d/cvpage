'''
This script is used to convert the resume data into a html file
of the standard template in ./standard/standard.html 
and its styles in ./results/style.css

'''

from bs4 import BeautifulSoup

'''
Function to fill the resume template with the data

input:
template_path: path to the template file (html file)
output_path: path to the output file (html file)
data: dictionary of the resume data

example data:
{
    "{NAME}": "DEV NARAYAN C B",
    "{EMAIL}": "dev@gmail.com",
    "{PHONE}": "8811231244",
}

'''

def handle_list_fill(soup_obj, place_text, values_list, css_style="margin-right: 20px;"):
    """
    Replace a placeholder element with a list of values in a BeautifulSoup object.

    Args:
        soup_obj (BeautifulSoup): The BeautifulSoup object representing the HTML content.
        place_text (str): The text content of the placeholder element to be replaced.
        values_list (list): A list of values to fill in place of the placeholder element.
        css_style (str, optional): CSS style to be applied to each list item. Defaults to "margin-right: 20px;".

    Example:
        # Assuming soup is a BeautifulSoup object representing an HTML document
        handle_list_fill(soup, "EXPERIENCE_PLACEHOLDER", ["Job 1", "Job 2", "Job 3"])

    """
    # Find the placeholder elements
    placeholder_element = soup_obj.find(text=place_text)

    if not placeholder_element:
        raise ValueError(f"Placeholder element with text '{place_text}' not found.")

    # Find the parent element of the skills placeholder
    parent_element = placeholder_element.find_parent()

    # Remove the existing placeholder element
    placeholder_element.extract()

    if len(values_list) == 0:
        # Handle case where values_list is empty
        list_element = soup_obj.new_tag('li', style=css_style)
        description_element = soup_obj.new_tag('p')
        description_element.string = "None           "
        list_element.append(description_element)
        parent_element.append(list_element)
    else:
        # Handle case where values_list is not empty
        for data in values_list:
            list_element = soup_obj.new_tag('li', style=css_style)
            description_element = soup_obj.new_tag('p')
            description_element.string = data
            list_element.append(description_element)
            parent_element.append(list_element)

def handle_skill_fill(soup_obj, place_text, values_list, css_style="margin-right: 20px;"):
    """
    Replace a placeholder element with a list of values in a BeautifulSoup object.

    Args:
        soup_obj (BeautifulSoup): The BeautifulSoup object representing the HTML content.
        place_text (str): The text content of the placeholder element to be replaced.
        values_list (list): A list of values to fill in place of the placeholder element.
        css_style (str, optional): CSS style to be applied to each list item. Defaults to "margin-right: 20px;".

    Example:
        # Assuming soup is a BeautifulSoup object representing an HTML document
        handle_list_fill(soup, "EXPERIENCE_PLACEHOLDER", ["Job 1", "Job 2", "Job 3"])

    """
    # Find the placeholder elements
    placeholder_element = soup_obj.find(text=place_text)

    if not placeholder_element:
        raise ValueError(f"Placeholder element with text '{place_text}' not found.")

    # Find the parent element of the skills placeholder
    parent_element = placeholder_element.find_parent()

    # Remove the existing placeholder element
    placeholder_element.extract()

    if len(values_list) == 0:
        # Handle case where values_list is empty
        list_element = soup_obj.new_tag('li', style=css_style)
        description_element = soup_obj.new_tag('h3')
        description_element.string = "None           "
        list_element.append(description_element)
        parent_element.append(list_element)
    else:
        # Handle case where values_list is not empty
        for data in values_list:
            print(data)
            list_element = soup_obj.new_tag('span',attrs={'class': 'skill-badge'})
            list_element.string = data + ",  "
            parent_element.append(list_element)
def fill_resume_template(template_path, output_path, data):
    # Read the HTML template
    with open(template_path, 'r', encoding='utf-8') as file:
        html_content = file.read()

    # Parse the HTML content
    soup = BeautifulSoup(html_content, 'html.parser')

    print("data",data)
    # Replace placeholder values with your custom data
    for placeholder, value in data.items():
        print("Replacing ",placeholder)
        if placeholder == "{IMAGE}":
            img_element = soup.find('img')
            print(img_element)
            
            if img_element:
                if value != None:
                    img_element['src'] = value
                else:
                    img_element['src'] = "images/profile.png"

        elif placeholder == "{DESIGNATION}":
                element = soup.find(text=placeholder)
                # Find the parent element of the skills placeholder
                parent_element = element.find_parent()

                # Remove the existing placeholder element
                element.extract()

                # Create a new list element for each skill
                if len(value) > 0:
                    for desg in value:
                        new_skill_element = soup.new_tag('h3')
                        new_skill_element.string = desg
                        parent_element.append(new_skill_element)
                else:
                    new_skill_element = soup.new_tag('h3')
                    new_skill_element.string = "Job seeker"
                    parent_element.append(new_skill_element)
        # Handle the experience section
        elif placeholder == "{EXPERIENCE}":
            '''
            The experience data is a list string 
            '''
            # # Find the placeholder elements
            experience_element = soup.find(text = "{EXPERIENCE}")
            # Find the parent element of the skills placeholder
            parent_element = experience_element.find_parent()
            exp_data_list = value
            # Remove the existing placeholder element
            experience_element.extract()

            for data in exp_data_list:
                experience_list_element = soup.new_tag('li', style="margin-right: 20px;")
                # Create a job description element
                job_description_element = soup.new_tag('p')
                job_description_element.string = data
                experience_list_element.append(job_description_element)
                parent_element.append(experience_list_element)
        elif placeholder == "{EDU_QUALIFS}":
            '''
            The experience data is a list string 
            '''
            # # Find the placeholder elements
            experience_element = soup.find(text = "{EDU_QUALIFS}")
            # Find the parent element of the skills placeholder
            parent_element = experience_element.find_parent()
            exp_data_list = value
            # Remove the existing placeholder element
            experience_element.extract()

            for data in exp_data_list:
                experience_list_element = soup.new_tag('li',style="margin-right: 20px;")
                # Create a job description element
                job_description_element = soup.new_tag('p')
                job_description_element.string = data
                experience_list_element.append(job_description_element)
                parent_element.append(experience_list_element)
                      
        elif placeholder == "{ACHIEVEMENTS}":
            '''
            The ACHIEVEMENTS data is a list string 
            '''
            # # Find the placeholder elements
            experience_element = soup.find(text = "{ACHIEVEMENTS}")
            # Find the parent element of the skills placeholder
            parent_element = experience_element.find_parent()
            exp_data_list = value
            # Remove the existing placeholder element
            experience_element.extract()

            for data in exp_data_list:
                experience_list_element = soup.new_tag('li',style="margin-right: 10px;")
                # Create a job description element
                job_description_element = soup.new_tag('p')
                job_description_element.string = data
                experience_list_element.append(job_description_element)
                parent_element.append(experience_list_element)    

        elif placeholder == "{CONTACT}":
            '''
            The ACHIEVEMENTS data is a list string 
            '''
            # # Find the placeholder elements
            experience_element = soup.find(text = "{CONTACT}")
            # Find the parent element of the skills placeholder
            parent_element = experience_element.find_parent()
            exp_data_list = value
            # Remove the existing placeholder element
            experience_element.extract()

            for data in exp_data_list:
                experience_list_element = soup.new_tag('li')
                # Create a job description element
                job_description_element = soup.new_tag('p')
                job_description_element.string = data
                experience_list_element.append(job_description_element)
                parent_element.append(experience_list_element) 
        elif placeholder ==  "{CERTIFICATIONS}":
            handle_list_fill(soup,"{CERTIFICATIONS}",value)
        elif placeholder == "{EXCS}":
            handle_list_fill(soup,placeholder,value)
        elif placeholder == "{LINKS}":
            handle_list_fill(soup,placeholder,value)
        elif placeholder == "{SKILLS}":
            handle_skill_fill(soup,placeholder,value)
        else:
            element = soup.find(text=placeholder)
            if element:
                element.replace_with(str(value))
            else:
                print("Placeholder not found: ", placeholder)

    

    # Save the modified HTML to a new file
    with open(output_path, 'w', encoding='utf-8') as output_file:
        output_file.write(str(soup))


