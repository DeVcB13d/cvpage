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
def fill_resume_template(template_path, output_path, data):
    # Read the HTML template
    with open(template_path, 'r', encoding='utf-8') as file:
        html_content = file.read()

    # Parse the HTML content
    soup = BeautifulSoup(html_content, 'html.parser')

    print("data",data)
    # Replace placeholder values with your custom data
    for placeholder, value in data.items():
        
        # If the placeholder is for skills, then create a list
        if placeholder == "{SKILLS}" and len(value) > 0:
                element = soup.find(text=placeholder)
                # Find the parent element of the skills placeholder
                parent_element = element.find_parent()

                # Remove the existing placeholder element
                element.extract()

                # Create a new list element for each skill
                for skill in value:
                    new_skill_element = soup.new_tag('li')
                    new_skill_element.string = skill
                    parent_element.append(new_skill_element)
        elif placeholder == "{SKILLS}" and len(value) == 0:
            element = soup.find(text=placeholder)
            # Find the parent element of the skills placeholder
            parent_element = element.find_parent()

            # Remove the existing placeholder element
            element.extract()
        elif placeholder == "{EDUCATION}" and len(value) > 0:
            element = soup.find(text=placeholder)
            # Find the parent element of the skills placeholder
            parent_element = element.find_parent()

            for edu in value:
                if type(edu) == tuple:
                    new_edu_element = soup.new_tag('li')
                    new_edu_element.string = edu[0] + " " + edu[1]
                    parent_element.append(new_edu_element)
                else:
                    new_edu_element = soup.new_tag('li')
                    new_edu_element.string = edu
                    parent_element.append(new_edu_element)

            # Remove the existing placeholder element
            element.extract()
        elif placeholder == "{IMAGE}":
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
        elif placeholder == "{LINKS}":
            element = soup.find(text=placeholder)
            # Find the parent element of the skills placeholder
            parent_element = element.find_parent()

            # Remove the existing placeholder element
            element.extract()
            if value :
                # Create a new list element for each skill
                for link in value:
                    new_link_element = soup.new_tag('p', style='font-size: 10px;')
                    new_link_element.string = link
                    parent_element.append(new_link_element)
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
                experience_list_element = soup.new_tag('li')
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
                experience_list_element = soup.new_tag('li')
                # Create a job description element
                job_description_element = soup.new_tag('p')
                job_description_element.string = data
                experience_list_element.append(job_description_element)
                parent_element.append(experience_list_element)
                      
            
        else:
            element = soup.find(text=placeholder)
            if element:
                element.replace_with(str(value))
            else:
                print("Placeholder not found: ", placeholder)

    

    # Save the modified HTML to a new file
    with open(output_path, 'w', encoding='utf-8') as output_file:
        output_file.write(str(soup))


