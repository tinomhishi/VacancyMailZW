This repo was built for the purposes of the Facebook App Review. Our application is simply a scripts that posts items on our
page directly from our websites database. A python script calls the facebook graph API to Post to our facebook page periodically.
At this point the app extracts no information from Facebooks Users, nor does it have any interaction beyond posting data and links.
The script is executed as a django command i.e `python manage.py facebook`. Tokens are stored in the settings file and are referenced by settings.PGE_TOKEN, for the page token and settings.PGE_ID for the page ID. Then:

1) graph = facebook.GraphAPI(settings.PGE_TOKEN, version=3.2) # create facebook graph object then
2) graph.put_object(settings.PGE_ID,'feed',message='{objects.data}, linkstowebsite')
