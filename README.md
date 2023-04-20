# Driver Incentive Program by "The Assemblers"
---
## Introduction 
This is a semester-long senior level praticum software engineering project that revolves around a <b>Truck Driver Incentive Program</b> and is team-based.
<br><b>Agile development methodologies</b> were followed, with routine sprints each week and team meetings for artifacts such as sprint planning, etc.
<br>It is a web application that simulates a platform for truck driver users to earn points and spend them on a sponsor-curated catalog.
<br>There are 3 distinct user types: <b>Driver</b>, <b>Sponsor</b> (representing a sponsor organization), and <b>Admin</b>.
Each user has their own curated experience on the platform, with different abilities given to each.

Our project is integrated directly with <b>AWS services</b> such as <b>EC2</b> (to host the program) and <b>RDS</b> (for our database, specifically using MySQL).
The project is written in Python, using Django as our web framework.
We had implemented the <b>eBaySDK</b> for our external API for getting products and information for our custom catalog for drivers.

## Getting Started
Prerequisite: <b>Must have [Python installed](https://www.python.org/downloads/).</b>
<br>```pip``` Packages install list: <br>(invoke by ```$ pip install <package_name>```)
1.	[Django](https://docs.djangoproject.com/en/4.2/topics/install/)
2.	[mysqlclient](https://pypi.org/project/mysqlclient/)
3.	[ebaysdk](https://pypi.org/project/ebaysdk/) <b>*</b>
---
## Build and Test
1. Navigate to the ```$ ../good_driver/``` Directory
2. Run: ```$ python manage.py runserver``` in that directory
3. It should give you an IP of where it is running off of with a port, so navigate there in your browser of choice.
---
<b>Credits</b>: TJ Heffner, Hayden Strong, Kevin Le, Josiah Lamont
---

If you want to learn more about the packages/APIs used for your own understanding, here are some helpful links:
- [eBaySDK](https://developer.ebay.com/api-docs/user-guides/static/finding-user-guide-landing.html) - We specifically only used the ```Finding``` Traditional API.
- [mysqlclient](https://docs.djangoproject.com/en/4.2/ref/databases/#mysql-notes)
- [Django](https://docs.djangoproject.com/en/4.2/)
---
<b>*</b> - Note: ebaysdk requires you to have your own sandbox/production credentials for the catalog to work.