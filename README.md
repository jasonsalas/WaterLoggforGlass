# Waterlogg - update your Fitbit profile via voice!
## A utility integrating Fitbit with Google Glass

![Waterlogg lets you update your Fitbit profile with Google Glass using voice commands](https://dl.dropboxusercontent.com/u/12019700/glass-dev/tester-images/waterlogg-in-action.jpg)

### Genesis
Fitbit is one of the most fun wearable computing devices around, and it's frequently used in Google Glass hackathons as the base for neat ideas. There are also several cool projects leveraging the Fitbit API, including:

- [m-distance by Vadim Zaliva](https://github.com/vzaliva/m-distance) (**open source!**)
- [Nurun's Fitbit Glassware](http://www.digitalforreallife.com/2013/09/fitbit-glassware/)
- [Fitbit/Glass Bridge](http://glassalmanac.com/new-app-connects-fitbit-google-glass/1812/)

Still, the one use case that wasn't working for me was having to repeatedly log intake in Fitbit's mobile and web apps gets laborious and often takes the user away from doing more important things. This is precisely the problem that Google Glass solves - decoupling you from technology and not taking you out of the moment! This simple App Engine-hosted service lets you use handsfree voice dictation to post updates everytime you hydrate, which updates your Fitbit profile.

### Usage
After you've granted access to your Google and Fitbit profiles, use the _"OK Glass...Post an update to...Waterlogg"_ command on Glass, and then speak the volume of water you've just consumed. It'll be reflected on your [Fitbit dashboard](https://www.fitbit.com/).
		
### Libraries
This Glassware uses the following libraries:

- [Google APIs Client Library for Python](https://developers.google.com/api-client-library/python/guide/aaa_oauth) to make authorized requests using OAuth 2.0 to the [Google Glass Mirror API](https://developers.google.com/glass/v1/reference/)
- [Temboo's Fitbit library](https://www.temboo.com/library/Library/Fitbit/) to manage the [OAuth 1.0 flow and credentials](https://wiki.fitbit.com/display/API/OAuth+Authentication+in+the+Fitbit+API) and communicate with the [Fitbit API](https://www.fitbit.com/dev/dev) 
- A forked version of [Alain Vongsouvahn's](https://plus.google.com/+AlainVongsouvanh) code from the [Quick Start Project for Python](https://github.com/googleglass/mirror-quickstart-python) to negotiate the Outh 2.0 dance
- [Google App Engine's Task Queue](https://cloud.google.com/appengine/docs/python/taskqueue/) to asynchronously handle notification pings from Google (in the log files, the user agent will be an HTTP-POST request from **"GlassAPI"**)

Using the Task Queue helps greatly with scalability and performance, as the multiple API calls to remote web services can imposes a tad bit of latency, which would add-up at scale. And you don't want delays at your callback URL.  Remember: **DON'T LET YOUR ENDPOINT BECOME YOUR CHOKEPOINT!**

_Disclaimer: This was written to be a personal utility, and due to API rate limits from Google, Fitbit, and Temboo, at the moment probably isn't ready to handle mass deployment requests. It isn't hard at all to scale it up, though, or use a different OAuth library. **Go for it!**_

---

You can find out more Glassware tips in my book, [Designing and Developing for Google Glass](http://www.amazon.com/Designing-Developing-Google-Glass-Differently/dp/1491946458), by O'Reilly & Associates. **Thanks for your support! :)**