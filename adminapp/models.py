from django.db import models

# Create your models here.
from django.db import models


# Create your models here.


class CnnModel(models.Model):
    S_No = models.AutoField(primary_key=True)
    model_accuracy = models.CharField(max_length=10)
    model_name = models.CharField(max_length=10)
    model_executed = models.CharField(max_length=10, null=True)

    class Meta:
        db_table = "Cnn_model"

        
        
class MobileNetModel(models.Model):
    S_No = models.AutoField(primary_key=True)
    model_accuracy = models.CharField(max_length=10)
    model_name = models.CharField(max_length=10)
    model_executed = models.CharField(max_length=10, null=True)

    class Meta:
        db_table = "MobileNet_model"




class DenseNetModel(models.Model):
    S_No = models.AutoField(primary_key=True)
    model_accuracy = models.CharField(max_length=10)
    model_name = models.CharField(max_length=10)
    model_executed = models.CharField(max_length=10, null=True)

    class Meta:
        db_table = "Densenet_model"



class ComparisonGraphModel(models.Model):
    S_No = models.AutoField(primary_key=True)
    Cnn = models.CharField(max_length=10, null=True)
    MobileNet = models.CharField(max_length=10, null=True)
    Densenet = models.CharField(max_length=10, null=True)

    class Meta:
        db_table = "Comparisongraph"



class Train_test_split_model(models.Model):
    S_No = models.AutoField(primary_key=True)
    Images_training = models.CharField(max_length=10, null=True)
    Images_validation = models.CharField(max_length=10, null=True)
    Images_testing = models.CharField(max_length=10, null=True)
    Images_classes = models.CharField(max_length=10, null=True)

    class Meta:
        db_table = "Traintestsplit"
