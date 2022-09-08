from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

User = get_user_model()


class Command(BaseCommand):
    """ Для создания супер юзера """

    def add_arguments(self, parser):
        parser.add_argument('user_name', type=str)
        parser.add_argument('password', type=str)

    def handle(self, *args, **kwargs):
        count = User.objects.all().count()
        if count == 0:
            User.objects.create_superuser(
                username=kwargs.get('user_name'),
                password=kwargs.get('password')
            )
            self.stdout.write(self.style.SUCCESS('Successfully create superuser "%s"'))
