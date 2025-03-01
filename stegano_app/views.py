import stepic
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from PIL import Image # importing the Image module from the PIL library.
import io
import os
# import image_steganography.ipynb   #importing the python script
from .models import EncryptedImage

# Create your views here.
@login_required
def index(request):
    return render(request, 'index.html')

@login_required
def about(request):
    return render(request, 'about.html')

def register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if len(password) < 3:
            messages.error(request, 'Password must be at least 3 characters!')
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Error, username already exists, use another!')
            return redirect('register')

        new_user = User.objects.create_user(username=username, email=email, password=password)
        new_user.save()

        messages.success(request, 'User successfully created, login now!')
        return redirect('login')

    return render(request, 'register.html', {})

def loginpage(request):
    if request.method == "POST":
        username = request.POST.get('uname')
        password = request.POST.get('pass')

        validate_user = authenticate(request, username=username, password=password)
        if validate_user is not None:
            login(request, validate_user)
            return redirect('index')
        else:
            messages.error(request, 'Error, wrong user details or user does not exist!')
            return redirect('login')

    return render(request, 'login.html', {})

def logoutview(request):
    logout(request)
    return redirect('login')

def hide_text_in_image(image, text):
    data = text.encode('utf-8')
    '''encode('utf-8') on a string, it translates the human-readable 
    characters into a sequence of bytes using the UTF-8 encoding.
     The result is a bytes object in Python.'''
    return stepic.encode(image, data)
#stepic.encode method is called to hide these bytes within the image


def encryption_view(request):
    message = ''
    encrypted_image_url = None
    if request.method == 'POST':
        text = request.POST['text']
        image_file = request.FILES['image']
        image = Image.open(image_file)

        # Convert to PNG if not already in that format
        if image.format != 'PNG':  # checks whether the image format is not PNG.
            image = image.convert('RGBA')
            # image is converted to RGBA mode if it's not already
            # This ensures the image has the correct color channels.
            buffer = io.BytesIO()
            # A BytesIO object is created,
            # which is a binary stream (an in-memory bytes buffer).
            image.save(buffer, format="PNG")
            image = Image.open(buffer)

        # hide text in image
        new_image = hide_text_in_image(image, text)

        # save the new image in a project folder
        image_path = 'project_folder/encrypted_images/' + 'new_' + image_file.name
        print("Image Path:", image_path)
        new_image.save(image_path, format="PNG")

        message = 'Text has been encrypted in the image.'
        
        download_filename = os.path.basename(image_path)

        # Create a response to download the image
        # with open(image_path, 'rb') as file:
        #     response = HttpResponse(file.read(), content_type='image/png')
        #     response['Content-Disposition'] = f'attachment; filename="{download_filename}"'

        # # Delete the image file after download
        # os.remove(image_path)
        encrypted_image_url = image_path
        
        # password = request.POST.get('password')
        
        # encrypted_image_obj = EncryptedImage.objects.create(image=image_file, password=password)
        # encrypted_image_obj.save()
        
        # return response
    return render(request, 'encryption.html', {'message': message, 'encrypted_image_url': encrypted_image_url})

def download_encrypted_image(request):
    if request.method == 'GET':
        encrypted_image_url = request.GET.get('encrypted_image_url')
        if encrypted_image_url:
            with open(encrypted_image_url, 'rb') as file:
                response = HttpResponse(file.read(), content_type='image/png')
                response['Content-Disposition'] = 'attachment; filename="encrypted_image.png"'
                return response
    return HttpResponse("Failed to download the encrypted image.")

def decryption_view(request):
    text = ''
    if request.method == 'POST':
        image_file = request.FILES['image']
        image = Image.open(image_file)

        # Convert to PNG if not already in that format
        if image.format != 'PNG':#checks whether the image format is not PNG.
            image = image.convert('RGBA')
            #image is converted to RGBA mode if it's not already
            #This ensures the image has the correct color channels.
            buffer = io.BytesIO()
            #A BytesIO object is created,
            # which is a binary stream (an in-memory bytes buffer).
            image.save(buffer, format="PNG")
            image = Image.open(buffer)

        # extract text from image
        text = extract_text_from_image(image)
        
        # decrypted_text = decrypt_text_from_image(image, password)
        # if decrypted_text is not None:
        #     text = decrypted_text
        # else:
        #     text = 'Decryption failed. Incorrect password or no hidden text found in the image.'


    return render(request, 'decryption.html', {'text': text})


def extract_text_from_image(image):
    data = stepic.decode(image)
    # uses the decode function from the stepic library to extract the
    # hidden data from the given image. This hidden data is
    # typically stored as bytes.
    if isinstance(data, bytes):
        return data.decode('utf-8')
    return data
