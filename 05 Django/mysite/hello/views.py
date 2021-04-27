from django.http import HttpResponse

# Used with template
# from django.shortcuts import get_list_or_404, render
# from .models import Label

data = {
    "Name"             : "Devon King",
    "Track"            : "Backend (Python)",
    "Message"          : "Thank you, mentors! You're all doing great!",
    "Active Course(s)" : ["Python: Introduction to Web Development"],
    "Completed Courses": ["Introduction to Cloud Computing",
                          "Basic Git: for complete beginners",
                          "Introduction to Programming",
                          "Software Development Life Cycle",
                          "Introduction to Database",
                          "HTTP, Secure Socket Layer Certificate and CORS",
                          "Python: Environment setup and Hello World",
                          "Python Syntax & Automated Teller Machine",
                          "Python: Loops & Functions",
                          "Python: Try...Except, Modules, Lambda and Files",
                          "Python: Object Oriented Programming"]
    }


def index(request):
    output = format_response(data)
    return HttpResponse(output)

    # # Used with hello/index.html template
    # # Use model to get Label info from db
    # label_list = get_list_or_404(Label)
    # # Use index.html to render webpage
    # return render(request, 'hello/index.html', {'label_list': label_list})


def format_response(dictionary: dict) -> str:
    """
    Format HTML response
    :param dictionary: The data to format
    :return: html response string
    """
    response = ""
    for key, value in dictionary.items():
        if type(value) is list:
            response += "<p><b>{} :</b><br />".format(key, value)
            for item in value:
                response += "&nbsp" * 10 + "{}<br />".format(item)
        else:
            response += "<p><b>{}:</b> {}</p>".format(key, value)
    return response
