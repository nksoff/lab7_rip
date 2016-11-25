import random

from django.core.management.base import BaseCommand, CommandError

from lab.models import Tutor, Course


class Command(BaseCommand):
    help = 'Generates tutors and courses'

    def handle(self, *args, **kwargs):
        for i in range(0, 10):
            t = Tutor.objects.create(lastname="Lastname " + str(i),
                                     firstname="Firstname " + str(i),
                                     middlename="Middlename " + str(i),
                                     birthday=str(random.randint(1950, 2000)) + "-09-01",
                                     sex=random.randint(1, 10) > 5)
            t.save()

            for j in range(0, random.randint(1, 6)):
                c = Course.objects.create(name="Course # {} of tutor {}".format(j, t.id),
                                          full_name="Course fullname",
                                          tutor=t)
                c.save()