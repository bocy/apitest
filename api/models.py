from django.db import models

# Create your models here.


class TestCase(models.Model):
    name = models.CharField(max_length=150)
    project = models.CharField(max_length=150)
    module = models.CharField(max_length=150)
    method = models.CharField(max_length=50)
    uri = models.CharField(max_length=100)
    params = models.TextField()
    dataformat = models.CharField(max_length=100)
    expects = models.TextField()
    create = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    headers = models.TextField()

    # objects = self.

    def __str__(self):
        return self.name


class TestRun(models.Model):
    caseid = models.IntegerField()
    casename = models.CharField(max_length=150)
    runtime = models.CharField(max_length=150)
    testresult = models.TextField()
    testsuite = models.CharField(max_length=100)
    request = models.TextField()
    response = models.TextField()

    def __str__(self):
        return self.casename


class TestServer(models.Model):
    name = models.CharField(max_length=150)
    protocol = models.CharField(max_length=50)
    ip = models.CharField(max_length=100)
    port = models.IntegerField()

    def __str__(self):
        return self.name


class TestSuite(models.Model):
    suitename = models.CharField(max_length=150)
    projects = models.CharField(max_length=150)
    caseids = models.CharField(max_length=200)
    casenames = models.TextField()
    serverid = models.IntegerField()


class SuiteResult(models.Model):
    suitename = models.CharField(max_length=150)
    project = models.CharField(max_length=150)
    testresult = models.CharField(max_length=50)
    passnumber = models.IntegerField()
    failnumber = models.IntegerField()
    successrate = models.FloatField()
    runtime = models.DateTimeField()
