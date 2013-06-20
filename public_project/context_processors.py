from public_project.models import Image


def uploaded_images_list(request):
    return { 'uploaded_images_list': Image.objects.all() }
    
    
