from django.db import models

from accounts.models import UserAccount, LabAccount
from initializer.models import visit
from patientProfiling.settings import BASE_DIR
"""Everything 'Test' in this file refers to lab test"""

class TestModel(models.Model):
    """ The Database Table for all available tests """

    testName = models.CharField(max_length=30, unique = True)
    unit = models.CharField(max_length=10)
    minVal = models.FloatField(null=True)
    maxVal = models.FloatField(null=True)

    def __str__(self):
        return self.testName

    class Meta:
        ordering = ['testName']


class TestItem (models.Model):
    """This actually represents multivalued attribute of 'User' Table
    in Database which records the lab tests the user has taken.
    
    ForeignKey => User associates test item to user.
    ForeignKey => TestModel selects test name.
    """
    visit_id = models.ForeignKey(visit, on_delete=models.CASCADE)
    testName = models.ForeignKey(TestModel, on_delete = models.PROTECT)
    result = models.FloatField(default=0)
    lab = models.ForeignKey(LabAccount, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.testName.testName


#Dummy Test Tags for Image Items
TAGS = [('Xray', 'X-Ray'), ('VXray', 'Video X-Ray'), ('Endoscopy','Endoscopy'), ('MRI', 'MRI')]

def user_dir_path(instance, filename):
    """ files will be uploaded to MEDIA_ROOT/user_<id>/filename """
    return 'user_{0}/reports/{1}'.format(instance.visit_id.user_id, filename)

class TestImage (models.Model):
    """ Model for any image report like X-ray,
    Endoscopy, Video X-ray """
    visit_id = models.ForeignKey(visit, on_delete=models.CASCADE)
    tag = models.CharField(max_length=20, choices=TAGS)
    image = models.ImageField(upload_to=user_dir_path)
    description = models.TextField(max_length=200, blank=True, null=True)
    lab = models.ForeignKey(LabAccount, on_delete=models.CASCADE)