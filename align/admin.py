from django.contrib import admin

from align.models import UploadFile, SingleJob, PairedJob, ImageTest

admin.site.register(SingleJob)

admin.site.register(PairedJob)

admin.site.register(UploadFile)

admin.site.register(ImageTest)

