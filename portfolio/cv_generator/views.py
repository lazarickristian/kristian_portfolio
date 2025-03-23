from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse
from django.template.loader import get_template, render_to_string
import json
from .forms import CVForm
import os
from django.conf import settings
import base64
import re
from datetime import datetime
from django.contrib import messages

def cv_generator(request):
    if not request.user.is_authenticated:
        messages.warning(request, "⚠️ You need to log in to access this page.")
        return redirect(reverse('login') + f'?next={request.path}')

    if request.method == "POST":
        form = CVForm(request.POST, request.FILES)
        if form.is_valid():
            # Get form data
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            profession = form.cleaned_data["profession"]
            city = form.cleaned_data["city"]
            country = form.cleaned_data["country"]
            email = form.cleaned_data["email"]
            phone = form.cleaned_data["phone"]
            summary = form.cleaned_data["summary"]
            photo = form.cleaned_data["photo"]
            skills_json = form.cleaned_data["skills"]  
            languages_json = form.cleaned_data["languages"]  
            work_experience_json = form.cleaned_data["work_experience"]
            educations_json = form.cleaned_data["education"]
            social_links_json = form.cleaned_data["social_links"]

            # Convert JSON string to a Python list
            skills = json.loads(skills_json) if skills_json else []
            languages = json.loads( languages_json) if languages_json else []
            work_experience = json.loads(work_experience_json) if work_experience_json else []
            educations = json.loads(educations_json) if educations_json else []
            social_links = json.loads(social_links_json) if social_links_json else []

            #Function to format date as "Jan 2012"
            def format_date(date_str):
                if date_str.lower() == "current":  # Handle "Current" as an end date
                    return "Current"
                try:
                    date_obj = datetime.strptime(date_str, "%Y-%m")  # Convert from "YYYY-MM"
                    return date_obj.strftime("%b %Y")  # Convert to "Jan 2012"
                except ValueError:
                    return date_str  # Return original if invalid

            #Convert all work experience dates
            for work in work_experience:
                work["start_date"] = format_date(work["start_date"])
                work["end_date"] = format_date(work["end_date"])

            #Convert all education dates
            for education in educations:
                education["edu_start_date"] = format_date(education["edu_start_date"])
                education["edu_end_date"] = format_date(education["edu_end_date"])

            #Sort work experience by start_date (most recent first)
            work_experience.sort(key=lambda x: datetime.strptime(x["start_date"], "%b %Y"), reverse=True)

            #Sort education by start_date (most recent first)
            educations.sort(key=lambda x: datetime.strptime(x["edu_start_date"], "%b %Y"), reverse=True)

            # Convert Image to Base64 (if uploaded)
            photo_base64 = None
            if photo:
                photo_base64 = base64.b64encode(photo.read()).decode("utf-8")
                photo_mime_type = photo.content_type  # Get image type (e.g., "image/png")

                # Create full Base64 string for embedding in HTML
                photo_src = f"data:{photo_mime_type};base64,{photo_base64}"
            else:
                photo_src = None  # No image uploaded

            # Load CV template and render HTML
            template = get_template("cv_generator/cv_template.html")
            html_content = template.render({
                "first_name": first_name,
                "last_name": last_name,
                "profession": profession,
                "city": city,
                "country": country,
                "email": email,
                "phone": phone,
                "summary": summary,
                "photo": photo_src,  
                "skills": skills,  
                "languages": languages,
                "work_experience": work_experience,
                "educations": educations,
                "social_links": social_links,
            })

            # Sanitize filename to remove special characters
            safe_first_name = re.sub(r'[^a-zA-Z0-9]', '', first_name)
            safe_last_name = re.sub(r'[^a-zA-Z0-9]', '', last_name)
            filename = f"{safe_first_name}_{safe_last_name}_cv.html"

            # Create a response with HTML file download
            response = HttpResponse(html_content, content_type="text/html")
            response["Content-Disposition"] = f'attachment; filename="{filename}"'
            return response
    else:
        form = CVForm()
    
    return render(request, "cv_generator/cv_generator.html", {"form": form})

