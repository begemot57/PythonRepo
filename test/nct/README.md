# FindAppointmentNCT.py

## What does it do

FindAppointmentNCT.py script allows you to specify your "reg number" and "month" where you want to get your appointment.  
Script runs in background and shows you the browser window when an appointment is found. This window will stay there for 10 mutes.
This is your chance to book an appointment and pay for it.  
In the first go you might manually go to the NCT page and check the month when first appointments ara available -
you can run the script using this month to see if it works as desired for you.

## Configuration

Put in your reg here
```
REGISTRATION = "12L1591"
```

Month for appointment: January, February, March etc.
```
TARGET_MONTH = "September"
```

***!!! NOTE !!!***   
In the script you can't specify location for the test, so it will default to the location that NCT office has set for you.  
Right now there is no way you can change this behavior.

***!!! NOTE !!!***   
Script was tested with Chrome browser. Selenium Chromedriver only supports Chrome version <= 116.  
Most likely your Chrome version will be higher than that.
This is how you can find your Chrome version:
- Open Chrome and click the three dots in the top-right corner.
- Go to "Settings" -> "About Chrome."

If your Chrome version is <= 116, do the following:
- Get chromedriver from here depending on your Chrome version: https://googlechromelabs.github.io/chrome-for-testing/#stable
- NOTE - you need "chromediriver". For Chrome 122 on ARM64 it will be this zip: https://storage.googleapis.com/chrome-for-testing-public/122.0.6261.128/mac-arm64/chromedriver-mac-arm64.zip
- You need to unzip it, right click on "chromedriver" and hit "open" for your Mac to trust it
- Put the path to your chromedriver in here:
DRIVER_PATH = "/path_to_chromedriver/chromedriver-mac-arm64/chromedriver"

## Run on Mac
```
> git clone https://github.com/begemot57/PythonRepo.git
> cd PythonRepo/test/nct 
> brew install python
> python3 --version
> python3 -m pip install selenium
# configure the script with your "reg", "month" and "chromedriver path"
# in the first run try the month with available appointments
> python3 FindAppointmentNCT.py
```