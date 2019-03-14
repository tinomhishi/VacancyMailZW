from django.core.management.base import BaseCommand
from django.core.mail import mail_managers
from django.utils import timezone
from django.conf import settings 
from datetime import timedelta

import facebook

from vacancy.models import Vacancy
from facebookbot.models import FacebookPost


class Command(BaseCommand):
	help = "Checking and Processing SMS Queue"

	def handle(self, *args, **options):
		self.stdout.write('Loading Facebook Posts....')
		self.create_batches()
		self.stdout.write('Sendig Posts....')
		self.post_vacancies()
		self.stdout.write('Posting Completed....')

	def create_batches(self):
		period = timezone.now = timedelta(days=1)
		vncies = Vacancy.objects.filter(created__gte=period, facebook=False,
						active=True, published=True).order_by('created')[0:100]

		for vncy in vncies:
			n = FacebookPost(vacancy=vncy)
			n.compose()
			vncy.facebook = True
			vncy.save()

	def post_vacancies(self):
		period = timezone.now() - timedelta(days=7)
		post_queue = FacebookPost.objects.filter(created__gte= period,
										published=False).order_by('created')[0:settings.FB_BATCH_SIZE]
		graph = facebook.GraphAPI(settings.PAGE_TOKEN, version=3.2)

		for post in post_queue:
			post.compose()
			self.stdout.write(('Post =>' + post.post)[0:50])
			self.stdout.write('Length =>' + str(len(post.post)))

			try:
				graph.put_object(settings.FB_PGE_ID, 'feed', message=post.post)
				post.published = True
				post.save()
			except:
				self.stdout.write('Error Posting on Facebook')
		self.stdout.write('Finishes sending posts....')		
				

