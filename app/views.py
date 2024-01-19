from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import Resume
from .checker import extract_and_compare

@csrf_exempt
def upload_resume(request):
    if request.method == 'POST':
        if 'file' in request.FILES:
            resume_file = request.FILES['file']
            # resume_text = resume_file.read().decode('utf-8')
            Resume.objects.create(file=resume_file)
            return JsonResponse({'message': 'Resume uploaded successfully'})
        else:
            return JsonResponse({'error': 'File not provided in the request'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)
        
@csrf_exempt
def suggestions(request):
    if request.method == 'POST':
        job_description = request.POST.get('job_description')

        if job_description:
            # Fetch the latest uploaded resume
            latest_resume = Resume.objects.last()

            if latest_resume:
                try:
                    # Read resume text with 'ignore' option for decoding
                    resume_text = latest_resume.file.read().decode('utf-8', errors='ignore')
                except UnicodeDecodeError as e:
                    # Handle the decoding error
                    return JsonResponse({'error': f'Error decoding resume text: {str(e)}'}, status=500)

                # Provide suggestions based on the latest resume text and the provided job description
                suggestions_text = extract_and_compare(resume_text, job_description)

                # Return JSON response
                response_data = {'job_description': job_description, 'suggestions': suggestions_text}
                return JsonResponse(response_data)
            else:
                return JsonResponse({'error': 'No resume uploaded yet'}, status=400)
        else:
            return JsonResponse({'error': 'Missing or empty "job_description" field in POST data'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)
