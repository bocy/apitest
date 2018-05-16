from django.db import models

# Create your models here.


class TestCase(models.Model):
    name = models.CharField(max_length=150)
    module = models.CharField(max_length=150)
    method = models.CharField(max_length=50)
    uri = models.CharField(max_length=100)
    params = models.TextField()
    expect = models.TextField()
    create = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    # objects = self.

    def __str__(self):
        return self.name

class TestRun(models.Model):
    caseid = models.IntegerField()
    casename = models.CharField(max_length=150)
    runtime = models.CharField(max_length=150)
    testresult = models.TextField()
    request = models.TextField()
    response = models.TextField()

    def __str__(self):
        return self.casename


class TestServer(models.Model):
    name = models.CharField(max_length=150)
    ip = models.CharField(max_length=100)
    port = models.IntegerField()

    def __str__(self):
        return self.name

