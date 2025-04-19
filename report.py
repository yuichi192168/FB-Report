import bs4               # For parsing HTML
import json              # For handling JSON data
import threading         # For running code in parallel threads
import cookielib         # Cookie handling for login sessions
import mechanize         # Simulates browser actions (login, submit forms, etc.)

# Create a class that reports a Facebook account
class Reports(threading.Thread):
    def __init__(self, email, pw, target):
        threading.Thread.__init__(self)  # Initialize thread
        self.email = email               # Facebook email
        self.pw = pw                     # Facebook password
        self.tg = target                 # Target user/page to report

    def run(self):
        # Initialize a simulated browser
        br = mechanize.Browser()
        url = "https://mbasic.facebook.com"  # Mobile site (simpler for automation)

        # Browser settings
        br.set_handle_equiv(True)
        br.set_handle_referer(True)
        br.set_handle_robots(False)
        br.set_cookiejar(cookielib.LWPCookieJar())  # Use cookie jar to manage session
        br.addheaders = [("User-Agent", "Mozilla/5.0 (Linux; U; Android 5.1)")]

        # Open Facebook mobile login page
        br.open(url)
        br.select_form(nr=0)
        br.form["email"] = self.email  # Fill in the email
        br.form["pass"] = self.pw      # Fill in the password
        br.submit()                    # Submit the login form

        # Go to the target's profile
        br.open("https://mbasic.facebook.com/{}".format(self.tg))
        soup = bs4.BeautifulSoup(br.response().read(), features="html.parser")

        # Find the "Report" link in the profile
        for link in soup.find_all("a", href=True):
            if "rapid_report" in link["href"]:
                report_link = link["href"]
                break

        # Open the report form
        br.open(report_link)
        br._factory.is_html = True

        # Prepare the data to be submitted (fake profile report)
        report_data = json.dumps({
            "fake": "profile_fake_account",
            "action_key": "FRX_PROFILE_REPORT_CONFIRMATION",
            "checked": "yes"
        })
        data = json.loads(report_data)

        # Select the reason: fake account
        br.select_form(nr=0)
        br.form["tag"] = [data["fake"]]
        br.submit()

        # Confirm action
        br._factory.is_html = True
        br.select_form(nr=0)
        try:
            br.form["action_key"] = [data["action_key"]]
        except:
            return False
        br.submit()

        # Final confirmation
        br._factory.is_html = True
        try:
            br.select_form(nr=0)
            br.form["checked"] = [data["checked"]]
            br.submit()
            result = br.response().read()

            # Check response
            if "Terima kasih atas masukan Anda." in result:
                print("[*] Reported.")
            else:
                print("[-] Unreported.")
        except:
            print("[-] Already Reported.")
