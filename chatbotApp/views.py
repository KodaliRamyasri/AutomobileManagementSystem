from django.shortcuts import render
from django.http import JsonResponse
from .models import ChatMessage

def home(request):
    return render(request, 'chatbotApp/home.html')

def chat(request):
    if request.method == 'POST':
        user_message = request.POST.get('message')
        response_message = get_chatbot_response(user_message)
        ChatMessage.objects.create(message=user_message, response=response_message)
        return JsonResponse({'message': user_message, 'response': response_message})
    return JsonResponse({'error': 'Invalid request method.'})

def get_chatbot_response(user_message):
    user_message = user_message.lower()
    if 'hey' in user_message:
        return (
            "Hello! How can we assist you today? Please choose one of the following options:\n"
            "1. What problems we can solve\n"
            "2. How to book an appointment\n"
            "3. Contact us\n"
            "4. Service pricing\n"
            "5. Operating hours\n"
            "6. Location and directions"
        )
    elif '1' in user_message or 'problems' in user_message:
        return (
            "We can solve a variety of vehicle problems, including:\n"
            "a. Engine issues\n"
            "b. Brake problems\n"
            "c. Transmission repairs\n"
            "d. Tire replacements\n"
            "e. Battery services\n"
            "f. Oil changes\n"
            "Please specify the problem you are facing by typing the corresponding letter."
        )
    elif 'a' in user_message:
        return "Engine issues can be complex. We offer diagnostics and repairs for various engine problems, including overheating, stalling, and performance issues. Schedule an appointment to get your engine checked."
    elif 'b' in user_message:
        return "We provide comprehensive brake services, including inspection, pad replacement, and repair of brake systems. Ensure your safety by having your brakes checked regularly."
    elif 'c' in user_message:
        return "Transmission repairs are crucial for vehicle performance. We handle everything from fluid changes to complete rebuilds. Contact us to discuss your transmission issues."
    elif 'd' in user_message:
        return "Tire replacements are essential for safety and performance. We offer a wide range of tire brands and sizes to suit your vehicle. Visit us to find the perfect tires for your car."
    elif 'e' in user_message:
        return "Battery services include testing, replacement, and maintenance. A reliable battery is vital for your vehicle. Come in for a battery check today."
    elif 'f' in user_message:
        return "Regular oil changes keep your engine running smoothly. We use high-quality oils and filters to ensure the best performance. Book an oil change with us."
    elif '2' in user_message or 'appointment' in user_message:
        return (
            "You can book an appointment through the following methods:\n"
            "- Visit our website and fill out the booking form\n"
            "- Call our customer service at (123) 456-7890\n"
            "Please specify the type of service you need to proceed with booking."
        )
    elif '3' in user_message or 'contact' in user_message:
        return (
            "You can contact us via the following methods:\n"
            "- Email: support@vehicleservice.com\n"
            "- Phone: (123) 456-7890\n"
            "Our customer service team is available from 9 AM to 6 PM, Monday to Friday. How else can we help you?"
        )
    elif '4' in user_message or 'pricing' in user_message:
        return (
            "Our service pricing is as follows:\n"
            "- Oil change: Rs 1500\n"
            "- Brake inspection: Rs 2500\n"
            "- Transmission repair: Starting at Rs 3000\n"
            "- Total repair: Starting at Rs 10000\n"
            "For a detailed pricing list, please visit our website or contact customer service."
        )
    elif '5' in user_message or 'hours' in user_message:
        return (
            "Our operating hours are:\n"
            "- Monday to Friday: 9 AM - 6 PM\n"
            "- Saturday: 10 AM - 4 PM\n"
            "- Sunday: Closed\n"
            "We look forward to serving you during these times."
        )
    elif '6' in user_message or 'location' in user_message:
        return (
            "We are located at Shop no.:124/34, Gachibowli, Hyderabad, Telangana. You can find us using the following directions:\n"
            "- From the gachibowli center, head north on Lanco Street for 2 kilometres.\n"
            "- We are on the right side, next to the gas station.\n"
            "For a detailed map, please visit our website."
        )
    else:
        return (
            "I'm sorry, I didn't understand that. Please choose one of the following options:\n"
            "1. What problems we can solve\n"
            "2. How to book an appointment\n"
            "3. Contact us\n"
            "4. Service pricing\n"
            "5. Operating hours\n"
            "6. Location and directions"
        )
