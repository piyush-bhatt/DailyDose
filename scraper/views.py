from django.shortcuts import render, redirect

from scraper.models import Subreddits
from .shared import scrape
from django.contrib import auth, messages
from django.contrib.auth.models import User
from django.core.mail import send_mail
from DailyDose import settings


# Create your views here.
def index(request):
    return render(request, 'scraper/index.html')


def login(request):
    try:
        if not request.POST.get('remember_me', None):
            request.session.set_expiry(0)
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, 'Login successful')
        else:
            messages.error(request, 'Login unsuccessful : Incorrect username or password')
    except:
        messages.error(request, 'Something went wrong. Please log in again.')
    finally:
        return redirect("/scraper/")

def logout(request):
    try:
        auth.logout(request)
        messages.success(request, 'Logout successful')
    except Exception as e:
        messages.error(request, 'Something went wrong. Please log out again.' + str(e))
    finally:
        return redirect("/scraper/")


def register(request):
    try:
        username = request.POST.get("usernameSignup")
        password = request.POST.get("password")
        password1 = request.POST.get("password1")
        email = request.POST.get("email")
        first_name = request.POST.get("firstName")
        last_name = request.POST.get("lastName")

        if password != password1:
            messages.error(request, "Sign up unsuccessful : Passwords don't match")
        elif User.objects.filter(username=username).exists():
            messages.error(request, "Sign up unsuccessful : Username is already taken")
        elif User.objects.filter(email=email).exists():
            messages.error(request, "Sign up unsuccessful : Email Id already in use")
        else:
            user = User.objects.create_user(username=username, email=email, first_name=first_name, last_name=last_name,
                                            password=password)
            if user is not None:
                auth.login(request, user)
                subreddit = Subreddits.objects.create(subreddit_name='all', user=user)
                if subreddit is not None:
                    subreddit.save()
                    messages.success(request, 'Sign up successful')
                else:
                    messages.error(request, 'Sign up successful but could not add subreddit')
                send_mail(
                    'Registered successfully',
                    'Hi ' + first_name + ',\nYou have successfully registered with Daily Dose.\n'
                                         'Thankyou for choosing us.',
                    settings.EMAIL_HOST_USER,
                    [email],
                    fail_silently=False,
                )
            else:
                messages.error(request, 'Sign up unsuccessful : Something went wrong')
    except Exception as e:
        messages.error(request, 'Something went wrong. Please sign up again.' + str(e))
    finally:
        return redirect("/scraper/")


def forgotPwd(request):
    try:
        email = request.POST.get("regEmail")
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            raw_password = User.objects.make_random_password()
            user.set_password(raw_password)
            user.save()
            send_mail(
                'Daily Dose Password',
                'Hi ' + user.first_name + ',\nYou have requested for your Daily Dose password reset.\n'
                'Please find the new password below.\n' + raw_password +
                '\nPlease change your password after login and report if this request was not made by you.',
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=False,
            )
            messages.success(request, 'Password sent successfully to provided email')
    except User.DoesNotExist:
        messages.error(request, 'No user with given email exists.')
    finally:
        return redirect("/scraper/")


def display(request, pk, sub):
    try:
        if pk == 'reddit':
            data = scrape.scrape_reddit(sub)
            context = {'data': data}
            return render(request, 'scraper/display_reddit.html', context)
        elif pk == 'gnews':
            data = scrape.scrape_gnews(sub)
            context = {'data': data}
            return render(request, 'scraper/display_gnews.html', context)
    except:
        messages.error(request, 'Unable to display')
        return redirect("/scraper/")


def profile(request, pk):
    try:
        if User.objects.filter(username=pk).exists():
            user = User.objects.get(username=pk)
            subreddits = Subreddits.objects.filter(user=user)
            return render(request, 'scraper/profile.html', {'user': user, 'subreddits': subreddits})
        else:
            messages.error(request, 'Unable to load profile')
            return redirect("/scraper/")
    except Exception as e:
        messages.error(request, 'Something went wrong'+str(e))
        return redirect("/scraper/")


def saveProfile(request):
    username = request.POST.get('username')
    try:
        user = User.objects.get(username=username)
        user.first_name = request.POST.get('firstName')
        user.last_name = request.POST.get('lastName')
        user.save()
    except:
        messages.error(request, 'Something went wrong.')
        return redirect("/scraper/")
    return redirect("/scraper/profile/" + user.username)


def addSubreddit(request, pk):
    user = User.objects.get(username=pk)
    try:
        subreddit_name = request.POST.get('subreddit')
        subreddit = Subreddits.objects.create(subreddit_name=subreddit_name, user=user)
        if subreddit is not None:
            subreddit.save()
    except:
        messages.error(request, 'Something went wrong. Please add again')
    finally:
        return redirect("/scraper/profile/"+user.username)


def deleteSubreddit(request, pk, sub):
    user = User.objects.get(username=pk)
    try:
        Subreddits.objects.filter(user=user).filter(subreddit_name=sub).delete()
    except:
        messages.error(request, 'Something went wrong. Please add again')
    finally:
        return redirect("/scraper/profile/"+user.username)
