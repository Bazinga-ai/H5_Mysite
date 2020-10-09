from django.db import models

# Create your models here.
class Recorder(models.Model):
    title = models.CharField(max_length=64, default='Unnamed Title')
    main_text = models.TextField()
    pub_date = models.DateTimeField('date published')
    is_bold = models.BooleanField(default=False)
    author = models.CharField(max_length=32, default='Unknown')

    ip = models.GenericIPAddressField(default='none')
    backup_info = models.CharField(max_length=128, default='none')

    password = models.CharField(max_length=20, default='0')

    def __str__(self):
        title = self.title
        main_text = self.main_text
        author = self.author
        time = self.pub_date

        res = 'Title: ' + title + '\nDetails: ' + main_text + '\nAuthor: ' + author + '\nTime: ' + time.__str__()
        
        return res


class FileRadar(models.Model):
    password = models.CharField(max_length=20, default='0')
    path = models.CharField(max_length=256, default='none')
    size = models.CharField(max_length=16, default='0')
    upload_date = models.DateTimeField('upload date')
    download_times = models.IntegerField(default=0)
    file_type = models.CharField(max_length=6, default='none')
    file_name = models.CharField(max_length=64, default='none')

    crc = models.CharField(max_length=64, default='none')

    author = models.CharField(max_length=32, default='Unknown')
    ip = models.GenericIPAddressField(default='none')
    
