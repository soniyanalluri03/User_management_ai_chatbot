import json              #Convert JSON data to Python dictionary
from django.http import JsonResponse       #Send JSON response back to frontend

from django.shortcuts import render, redirect, get_object_or_404  #html,url,error 404
from django.core.paginator import Paginator              #split data
from django.contrib import messages                      #success or error
from .models import profile                              #model name
from .forms import ProfileForm                           #forms name
import csv
from django.http import HttpResponse


from django.http import HttpResponse

def home(request):   #function-function name
    return HttpResponse("Hello MyApp")

# CREATE
def add_user(request):                                    #add new user
    if request.method == "POST":                          #to submit form
        form = ProfileForm(request.POST)                  #collect data & forms
        if form.is_valid():                               #which field identify
            form.save()                                   
            messages.success(request, "User added successfully")  #meassage when it is success
            return redirect('list_users')                         #duplicates prevent of data
    else:
        form = ProfileForm()

    return render(request, 'add_user.html', {'form': form})  #add html page to it


# READ + SEARCH + PAGINATION
def list_users(request):
    query = request.GET.get('q')
    users = profile.objects.all()

    if query:
        users = users.filter(gender__icontains=query)
    paginator = Paginator(users, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    age_groups = {
        "0-18": 0,
        "19-25": 0,
        "26-35": 0,
        "36-45": 0,
        "46+": 0
    }

    for user in profile.objects.all():
        age = user.age

        if age <= 18:
            age_groups["0-18"] += 1
        elif age <= 25:
            age_groups["19-25"] += 1
        elif age <= 35:
            age_groups["26-35"] += 1
        elif age <= 45:
            age_groups["36-45"] += 1
        else:
            age_groups["46+"] += 1


   #counting the legend data:--
    male_count = profile.objects.filter(
        gender__iexact='male'
    ).count()

    female_count = profile.objects.filter(
        gender__iexact='female'
    ).count()

    below_24 = profile.objects.filter(
        age__lt=24
    ).count()

    above_24 = profile.objects.filter(
        age__gte=24
    ).count()




    context = {
        'page_obj': page_obj,
        'categories': list(age_groups.keys()),
        'data': list(age_groups.values()),

        'male_count': male_count,
        'female_count': female_count,
        'below_24': below_24,
        'above_24': above_24,
    }

    return render(request, 'list_users.html', context)



# UPDATE
def edit_user(request, id):                        #edit given data
    user = get_object_or_404(profile, id=id)       #show error if there is no data
    form = ProfileForm(request.POST or None, instance=user) #update same recorded data

    if form.is_valid():                                #if it is ther it will show 
        form.save()
        messages.success(request, "User updated successfully")
        return redirect('list_users')

    return render(request, 'edit_user.html', {'form': form})


# DELETE
def delete_user(request, id):                                       #asking in which id the user i should del
    user = get_object_or_404(profile, id=id)
    user.delete()                                                   #delete user
    messages.success(request, "User deleted successfully")
    return redirect('list_users')


#charts-on;;;;
def age_chart(request):
    age_groups = {
        "0-18": 0,
        "19-25": 0,
        "26-35": 0,
        "36-45": 0,
        "46+": 0
    }
    users = profile.objects.all()
    for user in users:
        age = user.age
        if age <= 18:
            age_groups["0-18"] += 1
        elif age <= 25:
            age_groups["19-25"] += 1
        elif age <= 35:
            age_groups["26-35"] += 1
        elif age <= 45:
            age_groups["36-45"] += 1
        else:
            age_groups["46+"] += 1

    context = {
        'categories': list(age_groups.keys()),
        'data': list(age_groups.values())
    }
    return render(request, 'age_chart.html', context)


#chartbot
def chatbot(request):

    print("Request reached chatbot")
    print("Method:", request.method)

    if request.method == "POST":

        data = json.loads(request.body)
        message = data.get("message", "").lower().strip()

        print("User Message:", message)

        total_users = profile.objects.count()

        # Greeting
        if message in ["hi", "hello", "hey", "hii"]:

            reply = """
Hello 👋

I am your AI Assistant.

I can help you with:

• Total Users
• Male Users
• Female Users
• Oldest User
• Youngest User
• Download Male CSV
• Download Female CSV
• Open Age Chart
• Open User List

Type 'help' to see all commands.
"""

        # Help
        elif "help" in message or "what can you do" in message:

            reply = """
Available Commands:

• Total users
• How many users
• Male users
• Female users
• Oldest user
• Youngest user
• Download male csv
• Download female csv
• Show age chart
• Open user list
"""

        # Total Users
        elif (
            "total users" in message or
            "how many users" in message or
            "user count" in message or
            "number of users" in message
        ):

            reply = f"There are {total_users} users."

        # DOWNLOAD CONDITIONS MUST COME BEFORE MALE/FEMALE

        # Download Male CSV
        elif message == "download male csv":

            reply = """
        <a href="/myapp/preview-male/" target="_blank">
        📄 Preview Male Users CSV
        </a>
        """

        # Download Female CSV
        elif message == "download female csv":

            reply = """
        <a href="/myapp/preview-female/" target="_blank">
        📄 Preview Female Users CSV 
        </a>
        """     
        # Female Users
        elif (
            "female users" in message or
            "how many females" in message or
            "female count" in message or
            message == "female"
        ):

            count = profile.objects.filter(
                gender__iexact="female"
            ).count()

            reply = f"There are {count} female users."

        # Male Users
        elif (
            "male users" in message or
            "how many males" in message or
            "male count" in message or
            message == "male"
        ):

            count = profile.objects.filter(
                gender__iexact="male"
            ).count()

            reply = f"There are {count} male users."

        # Oldest User
        elif (
            "oldest user" in message or
            "old user" in message or
            "old users" in message
        ):

            user = profile.objects.order_by("-age").first()

            if user:
                reply = f"The oldest user is {user.age} years old."
            else:
                reply = "No users found."

        # Youngest User
        elif (
            "youngest user" in message or
            "young user" in message
        ):

            user = profile.objects.order_by("age").first()

            if user:
                reply = f"The youngest user is {user.age} years old."
            else:
                reply = "No users found."

        # Open Age Chart
        elif (
            "age chart" in message or
            "show chart" in message
        ):

            reply = """
<a href="/myapp/age-chart/" target="_blank">
📊 Open Age Chart
</a>
"""

        # Open User List
        elif (
            "user list" in message or
            "open user list" in message
        ):

            reply = """
<a href="/myapp/list/" target="_blank">
📋 Open User List
</a>
"""

        # Thanks
        elif (
            "thanks" in message or
            "thank you" in message
        ):

            reply = "You're welcome 😊"

        # Unknown Question
        else:

            reply = """
Sorry, I didn't understand that.

Type 'help' to see available commands.
"""

        print("AI Assistant Reply:", reply)

        return JsonResponse({
            "reply": reply
        })

    return JsonResponse({
        "reply": "Invalid request"
    })

# Download Male Users CSV
def download_male_csv(request):

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="male_users.csv"'

    writer = csv.writer(response)

    writer.writerow(['ID', 'Gender', 'Age', 'Height', 'Weight'])

    users = profile.objects.filter(gender__iexact='male')

    for user in users:
        writer.writerow([
            user.id,
            user.gender,
            user.age,
            user.height,
            user.weight
        ])

    return response


# Download Female Users CSV
def download_female_csv(request):

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="female_users.csv"'

    writer = csv.writer(response)

    writer.writerow(['ID', 'Gender', 'Age', 'Height', 'Weight'])

    users = profile.objects.filter(gender__iexact='female')

    for user in users:
        writer.writerow([
            user.id,
            user.gender,
            user.age,
            user.height,
            user.weight
        ])

    return response



#preview report
def preview_male(request):

    users = profile.objects.filter(
        gender__iexact='male'
    )

    return render(
        request,
        'preview_male.html',
        {'users': users}
    )


def preview_female(request):

    users = profile.objects.filter(
        gender__iexact='female'
    )

    return render(
        request,
        'preview_female.html',
        {'users': users}
    )
