from .forms import StoryForm
from django.http import JsonResponse
from rest_framework import status as st

def createStyle(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            #process form logic
            form = StoryForm(request.POST, request.FILES or None)
            if form.is_valid():
                new_style = form.save(commit=False)
                new_style.designer = request.user.designer
                new_style.save()
                context = {
                        'designer': new_style.designer.brand_name,
                        'title': new_style.title,
                        'description': new_style.description,
                        'images': new_style.images.url,
                        'price': new_style.asking_price
                        }
                return JsonResponse(context, status=st.HTTP_201_CREATED)
            
            return JsonResponse({"error": f"{form.errors}"}, statu=st.HTTP_400_BAD_REQUEST)
        return JsonResponse({"method": "Method not allowed"}, status=st.HTTP_405_METHOD_NOT_ALLOWED)
    return JsonResponse({"err": "You need to login"}, statu=st.HTTP_401_UNAUTHORIZED)