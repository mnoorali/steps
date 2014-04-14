from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

# Create your models here.

class Contact(models.Model):

    first_name = models.CharField(max_length=255,)
    last_name = models.CharField(max_length=255,)

    email = models.EmailField()

    owner = models.ForeignKey(User)

    def __str__(self):

        return ' '.join([
            self.first_name,
            self.last_name,
        ])

    def get_absolute_url(self):

        return reverse('contacts-view', kwargs={'pk': self.id})        

class Address(models.Model):

    contact = models.ForeignKey(Contact)
    address_type = models.CharField(max_length=10,)

    address = models.CharField(max_length=255,)
    city = models.CharField(max_length=255,)
    state = models.CharField(max_length=2,)
    postal_code = models.CharField(max_length=20,)

    class Meta:
        unique_together = ('contact', 'address_type',)

    def __str__(self):

        return str(self.contact)


class Events(models.Model):
    eventname = models.CharField(max_length=100,)
    eventdesc = models.CharField(max_length=100,)
    startdate = models.DateField()
    enddate = models.DateField()
    status = models.CharField(max_length=10,)

    def __str__(self):

        return self.eventname

class Groups(models.Model):
    groupname = models.CharField(max_length=50,null=True)
    groupleader = models.CharField(max_length=50,)

    def __str__(self):

        return self.groupname

class Members(models.Model):
    username = models.OneToOneField(User)
 
    first_name = models.CharField(max_length=25,)
    last_name = models.CharField(max_length=25,)
    groupname = models.CharField(max_length=25,null=True)

    def __str__(self):

        return ' '.join([
            self.first_name,
            self.last_name,
        ])

class Stepslog(models.Model):
    username = models.ForeignKey(User)
    stepsdate = models.DateField()
    steps = models.IntegerField(default=0)
    eventname = models.CharField(max_length=25,blank=True)
    
    class Meta:
        unique_together = ('username', 'stepsdate')

    def __str__(self):
        return str(' '.join([str(self.username), str(self.stepsdate), str(self.steps)]))

        