import spacy
from django.views.decorators.csrf import csrf_exempt
from app.models import Resume, JobDescription
from django.http import JsonResponse
import json
import PyPDF2
import docx
import os
import re

def extract_text_from_pdf(resume_file):
    text = ""
    with resume_file.open('rb') as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        num_pages = len(pdf_reader.pages)

        for page_num in range(num_pages):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()

    return text 

def extract_text_from_docx(resume_file):
    text = ""
    with resume_file.open('rb') as docx_file:
        doc = docx.Document(docx_file)
        for paragraph in doc.paragraphs:
            text += paragraph.text + '\n'

    return text

def extract_text_from_resume(resume_file):
    file_extension = os.path.splitext(resume_file.name)[1].lower()

    if file_extension == '.pdf':
        return extract_text_from_pdf(resume_file)
    elif file_extension == '.docx':
        return extract_text_from_docx(resume_file)
    else:
        # Handle other file types if needed
        return "Unsupported file type"



def extract_years_of_experience(resume_text):
    # Function to extract date ranges from resume text
    def extract_date_ranges(text):
        return re.findall(r'(\d{1,2}/\d{4}\b|\b\d{4}\b)\s*-\s*(Present|\d{1,2}/\d{4}\b|\b\d{4}\b)', text)

    # Filter out unwanted sections (e.g., education, other)
    work_experience_sections = re.split(r'\b(EDUCATION|OTHER)\b', resume_text, flags=re.IGNORECASE)

    date_ranges = []

    # Process each work experience section
    for section in work_experience_sections[0]:
        # Skip sections with non-work-related keywords
        if any(keyword in section.upper() for keyword in ['EDUCATION', 'OTHER']):
            continue

        date_ranges.extend(extract_date_ranges(section))

    print("Raw Date Ranges:", date_ranges)

    # Your logic to calculate total years of experience based on date ranges
    total_years_of_experience = 0

    for start_date, end_date in date_ranges:
        # Assuming date format is "MM/YYYY" or "Present"
        start_year, start_month = map(int, start_date.split('/'))
        end_year, end_month = map(int, end_date.split('/')) if end_date.lower() != 'present' else (2024, 1)

        total_years_of_experience += end_year - start_year + (end_month - start_month) / 12

    print(f'Total Years of Experience: {total_years_of_experience:.2f}')

    return total_years_of_experience


@csrf_exempt
def match_skills(request):
    if request.method == 'POST':
        try:
            resume_file = request.FILES['resume']
            job_description_text = request.POST['job_description']
            years_of_experience = int(request.POST['years_of_experience'])

            # Process the resume
            resume_text = extract_text_from_resume(resume_file)

            # Replace newline characters with actual newlines
            resume_text = resume_text.replace("\n", " ")

            # Remove brackets from the resume text
            resume_text = resume_text.replace("(", "").replace(")", "")

            # Process the job description
            job_description_skills = set(skill.strip(",") for skill in job_description_text.lower().split())

            # Convert the extracted skills from the resume to lowercase and split
            resume_skills_lower = set(resume_text.lower().split())

            # Find missing skills
            missing_skills = list(job_description_skills - resume_skills_lower)

            # Check if there are missing skills
            if not missing_skills:
                extracted_years_of_experience = extract_years_of_experience(resume_text)
                if extracted_years_of_experience is not None and extracted_years_of_experience < years_of_experience:
                    message = f'Your resume indicates {extracted_years_of_experience} years of experience, which is less than the required {years_of_experience} years.'
                else:
                    message = 'Your resume perfectly matches the job requirements!'
                response_data = {
                    'message': message,
                }
            else:
                # Check years of experience
                # Modify the logic based on your actual data extraction method
                extracted_years_of_experience = extract_years_of_experience(resume_text)
                if extracted_years_of_experience is not None and extracted_years_of_experience < years_of_experience:
                    message = f'Your resume indicates {extracted_years_of_experience} years of experience, which is less than the required {years_of_experience} years.'
                else:
                    message = 'Your resume is missing some skills required for this job.'

                # Prepare JSON response
                response_data = {
                    'message': message,
                    'missing_skills': missing_skills,
                }

            return JsonResponse(response_data)

        except Exception as e:
            return JsonResponse({'error': f'An error occurred: {str(e)}'})

    return JsonResponse({'error': 'Invalid Request'})
