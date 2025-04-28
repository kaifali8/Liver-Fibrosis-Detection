from django.shortcuts import render, redirect
from django.contrib import messages 
import urllib.request
from mainapp.models import *
from adminapp.models import *
from django.utils import timezone
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pytz
from datetime import datetime

# Create your views here.

def user_dashboard(req):
    user_id = req.session["user_id"]
    user = UserModel.objects.get(user_id=user_id)
    Feedbacks_users_count = Feedback.objects.all().count()
    all_users_count = UserModel.objects.all().count()

    if user.Last_Login_Time is None:
        IST = pytz.timezone("Asia/Kolkata")
        current_time_ist = datetime.now(IST).time()
        user.Last_Login_Time = current_time_ist
        user.save()
        return redirect("user_dashboard")

    return render(
        req,
        "user/user-dashboard.html",
        {
            # "predictions": prediction_count,
            "user_name": user.user_name,  
            "feedback_count": Feedbacks_users_count,
            "all_users_count": all_users_count,
        },
    )

    
def profile(req):
    user_id = req.session.get("user_id")
    if not user_id:
        messages.error(req, "User not logged in.")
        return redirect("login")

    user = UserModel.objects.get(user_id=user_id)

    if req.method == "POST":
        user.user_name = req.POST.get("username")
        user.user_age = req.POST.get("age")
        user.user_address = req.POST.get("address")
        user.user_contact = req.POST.get("mobile_number")
        user.user_email = req.POST.get("email")
        user.user_password= req.POST.get("password")
        # Handle image upload if present
        if 'profilepic' in req.FILES:
            user.user_image = req.FILES['profilepic']

        user.save()
        messages.success(req, "Profile updated successfully.")
        return redirect("profile")

    context = {"i": user}
    return render(req, "user/profile.html", context)



def user_feedback(req):
    id = req.session["user_id"]
    uusser = UserModel.objects.get(user_id=id)
    if req.method == "POST":
        rating = req.POST.get("rating")
        review = req.POST.get("review")
        if not rating or not review:
            messages.warning(req, "Enter all the fields to continue!")
            return render (req, "user/user-feedback.html")
        # print(sentiment)
        # print(rating)
        sid = SentimentIntensityAnalyzer()
        score = sid.polarity_scores(review)
        sentiment = None
        if score["compound"] > 0 and score["compound"] <= 0.5:
            sentiment = "positive"
        elif score["compound"] >= 0.5:
            sentiment = "very positive"
        elif score["compound"] < -0.5:
            sentiment = "negative"
        elif score["compound"] < 0 and score["compound"] >= -0.5:
            sentiment = " very negative"
        else:
            sentiment = "neutral"
        Feedback.objects.create(
            Rating=rating, Review=review, Sentiment=sentiment, Reviewer=uusser
        )
        messages.success(req, "Feedback recorded")
        return redirect("user_feedback")
    return render(req, "user/user-feedback.html")

def user_logout(req):
    if "user_id" in req.session:
        view_id = req.session["user_id"]
        try:
            user = UserModel.objects.get(user_id=view_id)
            user.Last_Login_Time = timezone.now().time()
            user.Last_Login_Date = timezone.now().date()
            user.save()
            messages.info(req, "You are logged out.")
        except UserModel.DoesNotExist:
            pass
    req.session.flush()
    return redirect("login")

# ------------------------------------------------------------------------------------------------------------
import os
import base64
from django.core.files.storage import default_storage
import numpy as np
import cv2
from django.conf import settings
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array


# Define the class mapping
class_dict = {
    0: 'F0',
    1: 'F1',
    2: 'F2',
    3: 'F3',
    4: 'F4',
}

def predict_image_category(model, image_path, model_type):
    try:
        # Preprocessing based on model type
        if model_type.lower() in ["cnn", "densenet"]:  # Models trained on 128x128 grayscale
            img = load_img(image_path, target_size=(128, 128), color_mode="grayscale")
            img_array = img_to_array(img)  # Shape: (128, 128, 1)
            img_array = np.expand_dims(img_array, axis=0)  # Shape: (1, 128, 128, 1)

        elif model_type.lower() == "mobilenet":  
            img = load_img(image_path, target_size=(224, 224), color_mode="grayscale")  
            img_array = img_to_array(img)  # Shape: (224, 224, 3)
            img_array = np.expand_dims(img_array, axis=0)  # Shape: (1, 224, 224, 3)

        else:
            raise ValueError("Unsupported model type. Use 'cnn', 'densenet', or 'mobilenet'.")

        # Normalize images
        img_array = img_array / 255.0

        # Debugging: Check input shape before prediction
        print(f"Model Type: {model_type}, Input Shape: {img_array.shape}, Expected: {model.input_shape}")

        # Model prediction
        predictions = model.predict(img_array)
        predicted_class = np.argmax(predictions, axis=1)[0]
        predicted_category = class_dict[predicted_class]

        return predicted_category

    except Exception as e:
        raise ValueError(f"Error in model prediction: {str(e)}")




def detection(req):
    print(f"Request method received: {req.method}")
    if req.method == "POST":
        print("Inside POST block")
        try:
            model_type = req.POST.get("model_type")
            print(model_type)
            uploaded_file = req.FILES.get("image")
            print(f"Model Type: {model_type}, Uploaded File: {uploaded_file}")

            if not model_type or not uploaded_file:
                print("Fields missing")
                messages.warning(req, "Enter all the fields to continue.....!")
                return render(req, "user/detection.html")

            temp_image_path = default_storage.save(uploaded_file.name, uploaded_file)
            image_path = default_storage.path(temp_image_path)
            

            if model_type == "Cnn":
                model_path = 'Liver Histopathology (Fibrosis) Ultrasound Images\cnn_model.h5'
                model = load_model(model_path)
                predicted_result = predict_image_category(model, image_path, model_type)
                model_info = CnnModel.objects.latest('S_No')
            elif model_type == "Mobilenet":
                model_path = 'Liver Histopathology (Fibrosis) Ultrasound Images\mobilnet_model (1).h5'
                model = load_model(model_path)
                predicted_result = predict_image_category(model, image_path, model_type)
                model_info = MobileNetModel.objects.latest('S_No')
            elif model_type == "Densenet":
                model_path = 'Liver Histopathology (Fibrosis) Ultrasound Images\densenet_model.h5'
                model = load_model(model_path)
                predicted_result = predict_image_category(model, image_path, model_type)
                model_info = DenseNetModel.objects.latest('S_No')
            else:
                raise ValueError("Select a valid Model")
            
            uploaded_image_base64, segmented_image_base64, grayscale_image_base64 = generate_segmented_image(image_path)

            req.session["image_path"] = default_storage.url(temp_image_path)
            req.session["predicted_result"] = predicted_result
            req.session["uploaded_image_base64"] = uploaded_image_base64
            req.session["segmented_image_base64"] = segmented_image_base64
            req.session["grayscale_image_base64"] = grayscale_image_base64
            req.session["model_name"] = model_info.model_name
            req.session["model_accuracy"] = model_info.model_accuracy
            messages.success(req, "Detection Process Completed")
            return redirect("detection_result")

        except Exception as e:
            print(f"Exception occurred: {e}")
            messages.error(req, f"An error occurred: {str(e)}")
            return render(req, "user/detection.html", {"error": str(e)})

    print("Inside ELSE block")
    return render(req, "user/detection.html")


def generate_segmented_image(image_path):
    image = cv2.imread(image_path)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, binary_image = cv2.threshold(gray_image, 127, 255, cv2.THRESH_BINARY)
    
    segmented_image_path = os.path.join(settings.MEDIA_ROOT, 'segmented_image.jpg')
    cv2.imwrite(segmented_image_path, binary_image)
    
    grayscale_image_path = os.path.join(settings.MEDIA_ROOT, 'grayscale_image.jpg')
    cv2.imwrite(grayscale_image_path, gray_image)
    
    with open(image_path, "rb") as img_file:
        original_image_base64 = base64.b64encode(img_file.read()).decode('utf-8')
    
    with open(segmented_image_path, "rb") as img_file:
        segmented_image_base64 = base64.b64encode(img_file.read()).decode('utf-8')
    
    with open(grayscale_image_path, "rb") as img_file:
        grayscale_image_base64 = base64.b64encode(img_file.read()).decode('utf-8')
    
    return original_image_base64, segmented_image_base64, grayscale_image_base64



def detection_result(req):
    image_path = req.session.get("image_path", None)
    predicted_result = req.session.get("predicted_result", "Unknown")
    model_accuracy = req.session.get("model_accuracy", None)
    model_name = req.session.get("model_name", None)
    uploaded_image_base64 = req.session.get("uploaded_image_base64", None)
    segmented_image_base64 = req.session.get("segmented_image_base64", "")
    grayscale_image_base64 = req.session.get("grayscale_image_base64", "")
    graph_accuracy = ""
    graph_loss = ""

    brief_note = {
        'F0': {
            'title': "No Fibrosis",
            'description': "The liver appears completely healthy with no visible signs of scarring or fibrosis. The tissue structure remains intact, and there is no disruption to liver function or blood flow. Patients at this stage do not exhibit any fibrosis-related symptoms, and normal liver function is maintained."
        },

        'F1': {
            'title': "Mild Fibrosis",
            'description': "Early-stage fibrosis is present, characterized by minimal scarring of liver tissue. At this stage, the connective tissue begins to thicken slightly, but there is no significant impact on liver function or blood flow. This stage is often asymptomatic, but it indicates the beginning of liver tissue damage, which may progress if the underlying cause is not addressed."
        },

        'F2': {
            'title': "Moderate Fibrosis",
            'description': "The liver shows moderate scarring, where fibrous tissue extends between portal areas. Some blood flow within the liver may be affected, leading to mild functional impairment. Although the liver can still perform its essential functions, this stage marks a significant progression from mild fibrosis and may begin to cause subtle symptoms like fatigue or mild discomfort. Without intervention, fibrosis can advance further."
        },

        'F3': {
            'title': "Severe Fibrosis",
            'description': "Extensive fibrotic tissue is present, bridging between different regions of the liver. The formation of fibrous septa disrupts the normal architecture of the liver, significantly impairing blood circulation. Patients may experience noticeable symptoms such as jaundice, abdominal swelling, or fatigue. At this stage, the risk of liver cirrhosis and other complications increases, making medical intervention crucial."
        },

        'F4': {
            'title': "Cirrhosis",
            'description': "This is the most advanced stage of fibrosis, where widespread scarring has replaced healthy liver tissue. The liver becomes stiff and nodular, severely affecting its ability to function properly. Blood flow is heavily compromised, leading to complications such as portal hypertension, fluid accumulation (ascites), and increased risk of liver failure. Cirrhosis is often irreversible, requiring close medical management and, in severe cases, a liver transplant may be necessary."
        }
    }
    predicted_note = brief_note.get(predicted_result, "No additional information available for this condition.")
    
    if model_name == "CNN":
        graph_accuracy = 'user/img/cnn_accuracy.jpg'
        graph_loss = 'user/img/cnn_loss.jpg'
    elif model_name == "Mobilenet":
        graph_accuracy = 'user/img/mobilenet_accuracy.jpg'
        graph_loss = 'user/img/mobilenet_loss.jpg'
    elif model_name == "densenet":
        graph_accuracy = 'user/img/densenet_accuracy.jpg'
        graph_loss = 'user/img/densenet_loss.jpg'

    return render(
        req,
        "user/detection-result.html",
        {
            "image_path": image_path,
            "predicted_label": predicted_result,
            "predicted_note": predicted_note,
            "model_accuracy": model_accuracy,
            "model_name": model_name,
            "uploaded_image_base64": uploaded_image_base64,
            "segmented_image_base64": segmented_image_base64,
            "grayscale_image_base64": grayscale_image_base64,
            "graph_accuracy": graph_accuracy,
            "graph_loss": graph_loss
        },
    )