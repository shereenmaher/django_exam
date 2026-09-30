from django.shortcuts import render , HttpResponse,redirect
from .models import *
from django.contrib import messages 
from datetime import date

#Landing Page(Register & login)
def index(request):
    return render(request,"index.html")

def register(request):

    if request.method == "POST":

        errors = User.objects.reg_validation(request.POST)

        if len(errors) > 0:

            context = {
                "errors": errors
            }

            return render(request, "index.html", context)

        else:

            user = User.objects.create_user(request.POST)

            request.session["user_id"] = user.id

            return render(request, "shows.html")
            

    else:

        return redirect("/")

def login(request):

    if request.method == "POST":

        errors = User.objects.log_validation(request.POST)

        if len(errors) > 0:

            context = {
                "errors": errors
            }

            return render(request, "index.html", context)

        else:

            user = User.objects.login_user(request.POST)

            request.session["user_id"] = user.id

            return render(request, "shows.html")

    else:

        return redirect("/")

def shows(request):

    if "user_id" not in request.session:

        return redirect("/")

    else:

        user = User.objects.get(
            id=request.session["user_id"]
        )

        shows = Show.objects.all()

        context = {
            "user": user,
            "shows": shows
        }

        return render(request,"shows.html",context)

def create_show(request):

    if "user_id" not in request.session:

        return redirect("/")

    else:

        user = User.objects.get(
            id=request.session["user_id"]
        )

        if request.method == "POST":

            errors = Show.objects.show_validation(request.POST)

            if len(errors) > 0:

                context = {
                    "user": user,
                    "errors": errors
                }

                return render(
                    request,
                    "create.html",
                    context
                )

            else:

                Show.objects.create_show(
                    request.POST,
                    user
                )

                return redirect("/shows/")

        else:

            context = {
                "user": user
            }

            return render(
                request,
                "create.html",
                context
            )

def view_show(request, show_id):

    if "user_id" not in request.session:

        return redirect("/")

    else:

        user = User.objects.get(
            id=request.session["user_id"]
        )

        show = Show.objects.get(
            id=show_id
        )

        context = {
            "user": user,
            "show": show
        }

        return render(
            request,
            "view.html",
            context
        )

def edit_show(request, show_id):

    if "user_id" not in request.session:

        return redirect("/")

    else:

        user = User.objects.get(
            id=request.session["user_id"]
        )

        show = Show.objects.get(
            id=show_id
        )

        if show.user.id != user.id:

            return redirect("/shows")

        if request.method == "POST":

            errors = Show.objects.show_validation(
                request.POST
            )

            if len(errors) > 0:

                context = {
                    "user": user,
                    "show": show,
                    "errors": errors
                }

                return render(
                    request,
                    "edit.html",
                    context
                )

            else:

                Show.objects.update_show(show,request.POST)

                return redirect("/shows")

        else:

            context = {
                "user": user,
                "show": show
            }

            return render(
                request,
                "edit.html",
                context
            )

def delete_show(request, show_id):

    if "user_id" not in request.session:

        return redirect("/")

    else:

        user = User.objects.get(
            id=request.session["user_id"]
        )

        show = Show.objects.get(
            id=show_id
        )

        if show.user.id == user.id:

            show.delete()

        return redirect("/shows")


def logout(request):

    request.session.flush()

    return redirect("/")
