from django.shortcuts import render, redirect
from django.contrib import messages 
import urllib.request
from adminapp.models import *
from mainapp.models import *
from django.core.paginator import Paginator
from django.utils.timezone import localtime

# Create your views here.
def admin_dash(req):
    # Fetch the last 4 recent users ordered by 'date_time' in descending order
    recent_users = UserModel.objects.all().order_by('-Date_Time')[:4]

    # Count statistics
    all_users_count = UserModel.objects.all().count()
    pending_users_count = UserModel.objects.filter(User_Status="pending").count()
    rejected_users_count = UserModel.objects.filter(User_Status="removed").count()
    accepted_users_count = UserModel.objects.filter(User_Status="accepted").count()
    feedbacks_users_count = Feedback.objects.all().count()
    classification_count = UserModel.objects.all().count()

    # Format the date and time for each user
    formatted_users = []
    for user in recent_users:
        formatted_users.append({
            'user_image': user.user_image,
            'user_name': user.user_name,
            'user_email': user.user_email,
            'date_time': localtime(user.Date_Time).strftime('%H:%M %d/%m/%Y')
        })

    return render(
        req,
        "admin/admin-dashboard.html",
        {
            "all_users": all_users_count,
            "pending_users": pending_users_count,
            "rejected_users": rejected_users_count,
            "accepted_users": accepted_users_count,
            "recent_users": formatted_users,
            "feedback_count": feedbacks_users_count,
            "classification_count": classification_count,
        },
    )

def cnn(req):
    model_name = "CNN"
    accuracy = "97.8"
    executed = "Executed!"

    try:
        model_performance = CnnModel.objects.get(model_name=model_name)
        model_performance.model_accuracy = accuracy
        model_performance.model_executed = executed
    except CnnModel.DoesNotExist:
        model_performance = CnnModel(
            model_name=model_name, model_accuracy=accuracy, model_executed=executed
        )
    model_performance.save()

    req.session["model_name"] = model_name
    req.session["accuracy"] = accuracy
    req.session["executed"] = executed
    return render(req,"admin/cnn.html")

def cnnresult(req):
    model_name = req.session.get("model_name")
    accuracy = req.session.get("accuracy")
    executed = req.session.get("executed")

    context = {"model_name": model_name, "accuracy": accuracy, "executed": executed}
    messages.success(req, "CNN Model executed successfully")
    return render(req,"admin/cnn-result.html",context) 

def densenet(req):
    model_name = "densenet"
    accuracy = "84"
    executed = "Executed"

    try:
        model_performance = DenseNetModel.objects.get(model_name=model_name)
        model_performance.model_accuracy = accuracy
        model_performance.model_executed = executed
    except DenseNetModel.DoesNotExist:
        model_performance = DenseNetModel(
            model_name=model_name, model_accuracy=accuracy, model_executed=executed
        )
    model_performance.save()

    req.session["model_name"] = model_name
    req.session["accuracy"] = accuracy
    req.session["executed"] = executed
    return render(req,"admin/densenet.html")

def densenetresult(req):
    model_name = req.session.get("model_name")
    accuracy = req.session.get("accuracy")
    executed = req.session.get("executed")

    context = {"model_name": model_name, "accuracy": accuracy, "executed": executed}
    messages.success(req, "densenet Model executed successfully")
    return render(req,"admin/densenet-result.html",context)

def mobilenet(req):
    model_name = "Mobilenet"
    accuracy = "78.1"
    executed = "Executed!"

    try:
        model_performance = MobileNetModel.objects.get(model_name=model_name)
        model_performance.model_accuracy = accuracy
        model_performance.model_executed = executed
    except MobileNetModel.DoesNotExist:
        model_performance = MobileNetModel(
            model_name=model_name, model_accuracy=accuracy, model_executed=executed
        )
    model_performance.save()

    req.session["model_name"] = model_name
    req.session["accuracy"] = accuracy
    req.session["executed"] = executed
    return render(req,"admin/mobilnet.html")

def mobilenetresult(req):
    model_name = req.session.get("model_name")
    accuracy = req.session.get("accuracy")
    executed = req.session.get("executed")

    context = {"model_name": model_name, "accuracy": accuracy, "executed": executed}
    messages.success(req, "Mobilenet Model executed successfully")
    return render(req,"admin/mobilnet-result.html",context)

def pendingusers(req):
    pending = UserModel.objects.filter(User_Status="pending")
    paginator = Paginator(pending, 5)
    page_number = req.GET.get("page")
    post = paginator.get_page(page_number)
    return render(req, "admin/pending-users.html", {"user": post})

def datasetoverview(req):
    images_training = "5,058"
    images_validation = 633
    images_testing = 632
    image_classes = "5 [F0,F1,F2,F3,F4]" 

    try:
        model_performance = Train_test_split_model.objects.latest("S_No")
        model_performance.Images_training = str(images_training)
        model_performance.Images_validation = str(images_validation)
        model_performance.Images_testing = str(images_testing)
        model_performance.Images_classes = str(image_classes)
    except Train_test_split_model.DoesNotExist:
        model_performance = Train_test_split_model(
            Images_training=str(images_training),
            Images_validation=str(images_validation),
            Images_testing=str(images_testing),
            Images_classes=str(image_classes),
        )

    model_performance.save()

    req.session["images_training"] = images_training
    req.session["images_validation"] = images_validation
    req.session["images_testing"] = images_testing
    req.session["image_classes"] = image_classes
    return render(req,"admin/dataset-overview.html")

def datasetinfo(req):
    latest_entry = Train_test_split_model.objects.latest("S_No")

    context = {
        "images_training": latest_entry.Images_training,
        "images_validation": latest_entry.Images_validation,
        "images_testing": latest_entry.Images_testing,
        "image_classes": latest_entry.Images_classes,
    }

    messages.success(req, "Dataset executed successfully")
    return render(req,"admin/dataset-info.html",context)

def testsplit(req):
    images_training = "5,058"
    images_validation = 633
    images_testing = 632
    image_classes = "5 [F0,F1,F2,F3,F4]" 

    try:
        model_performance = Train_test_split_model.objects.latest("S_No")
        model_performance.Images_training = str(images_training)
        model_performance.Images_validation = str(images_validation)
        model_performance.Images_testing = str(images_testing)
        model_performance.Images_classes = str(image_classes)
    except Train_test_split_model.DoesNotExist:
        model_performance = Train_test_split_model(
            Images_training=str(images_training),
            Images_validation=str(images_validation),
            Images_testing=str(images_testing),
            Images_classes=str(image_classes),
        )

    model_performance.save()

    req.session["images_training"] = images_training
    req.session["images_validation"] = images_validation
    req.session["images_testing"] = images_testing
    req.session["image_classes"] = image_classes
    return render(req,"admin/test-split.html")


def testsplitresult(req):
    latest_entry = Train_test_split_model.objects.latest("S_No")

    context = {
        "images_training": latest_entry.Images_training,
        "images_validation": latest_entry.Images_validation,
        "images_testing": latest_entry.Images_testing,
        "image_classes": latest_entry.Images_classes,
    }

    messages.success(req, "Train Test Split executed successfully")
    return render(req,"admin/test-split-result.html",context)


def graphcomparison(req):
    cnn = CnnModel.objects.last()
    mobilenet = MobileNetModel.objects.last()
    densenet = DenseNetModel.objects.last()

    cnn_graph = cnn.model_accuracy if cnn else "N/A"
    mobilenet_graph = mobilenet.model_accuracy if mobilenet else "N/A"
    densenet_graph = densenet.model_accuracy if densenet else "N/A"

    return render(
        req,
        "admin/graph-comparison.html",
        {
            "cnn": cnn_graph,
            "mobilenet": mobilenet_graph,
            "densenet": densenet_graph,
        },
    )

def adminlogout(req):
    messages.info(req, "You are logged out.")
    return redirect("adminlogin")

def allusers(req):
    all_users = UserModel.objects.all()
    paginator = Paginator(all_users, 5)
    page_number = req.GET.get("page")
    post = paginator.get_page(page_number)
    return render(req, "admin/all-users.html", {"allu": all_users, "user": post})


def delete_user(req, user_id):
    try:
        user = UserModel.objects.get(user_id=user_id)
        user.delete()
        messages.warning(req, "User was deleted successfully!")
    except UserModel.DoesNotExist:
        messages.error(req, "User does not exist.")
    except Exception as e:
        messages.error(req, f"An error occurred: {str(e)}")
    
    return redirect("allusers")


# Acept users button
def accept_user(req, id):
    try:
        status_update = UserModel.objects.get(user_id=id)
        status_update.User_Status = "accepted"
        status_update.save()
        messages.success(req, "User was accepted successfully!")
    except UserModel.DoesNotExist:
        messages.error(req, "User does not exist.")
    except Exception as e:
        messages.error(req, f"An error occurred: {str(e)}")
    
    return redirect("pendingusers")


# Remove user button
def reject_user(req, id):
    status_update2 = UserModel.objects.get(user_id=id)
    status_update2.User_Status = "removed"
    status_update2.save()
    messages.warning(req, "User was Rejected..!")
    return redirect("pendingusers")

# Change status users button
def change_status(req, id):
    user_data = UserModel.objects.get(user_id=id)
    if user_data.User_Status == "removed":
        user_data.User_Status = "accepted"
        user_data.save()
    elif user_data.User_Status == "accepted":
        user_data.User_Status = "removed"
        user_data.save()
    elif user_data.User_Status == "pending":
        messages.info(req, "Accept the user first..!")
        return redirect ("allusers")
    messages.success(req, "User status was changed..!")
    return redirect("allusers")

def feedback(req):
    feed = Feedback.objects.all()
    return render(req, "admin/feedback.html", {"back": feed})


def sentimentanalysis(req):
    fee = Feedback.objects.all()
    return render(req, "admin/sentiment-analysis.html", {"cat": fee})


def sentimentanalysisgraph(req):
    positive = Feedback.objects.filter(Sentiment="positive").count()
    very_positive = Feedback.objects.filter(Sentiment="very positive").count()
    negative = Feedback.objects.filter(Sentiment="negative").count()
    very_negative = Feedback.objects.filter(Sentiment="very negative").count()
    neutral = Feedback.objects.filter(Sentiment="neutral").count()
    context = {
        "vp": very_positive,
        "p": positive,
        "neg": negative,
        "vn": very_negative,
        "ne": neutral,
    }
    return render(req, "admin/sentiment-analysis-graph.html", context)

