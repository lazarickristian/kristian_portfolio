from django.views import View
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings
from .models import Message

def index(request):
  return render(request, 'about/index.html')

def about(request):
  return render(request, 'about/about.html')

def website(request):
  return render(request, 'about/website.html')

#def contact(request):
class ContactView(View):
  template_name = "about/contact.html"

  def get(self, request):
    return render(request, "about/contact.html")

  def post(self, request):

    def create_message_object(name, email, subject, message):
      Message.objects.create(
          name=name,
          email=email,
          subject=subject,
          message=message
      )

    name = request.POST.get("name")
    email = request.POST.get("email")
    subject = request.POST.get("subject")
    message = request.POST.get("message")

    if not (name and email and subject and message):
      messages.error(request, "All fields are required.")
      return redirect("contact")

    # Construct email content
    email_subject = f"New Contact Form Submission: {subject}"
    email_body = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"

    try:
        send_mail(
            subject=email_subject,
            message=email_body,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[settings.EMAIL_HOST_USER],
            fail_silently=False,
        )
        messages.success(request, "Your message has been sent. Thank you!")
        create_message_object(name, email, subject, message)
    except Exception as e:
        messages.error(request, "Your message could not been send !!!")
        #messages.error(request, f"An error occurred: {str(e)}")

    return redirect("contact")







def login(request):
    return render(request, 'about/login.html')
