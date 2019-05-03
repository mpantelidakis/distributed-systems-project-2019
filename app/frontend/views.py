from django.shortcuts import render

# Create your views here.
def HomePageView(request):
    """Homepage view"""
    return render(request, template_name='frontend/homepage.html')

# def LoginView(request):
#     """LoginView view"""
#     return render(request, template_name='frontend/login.html')

# def SignupView(request):
#     """Signup view"""
#     return render(request, template_name='frontend/signup.html')