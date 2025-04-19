from bs4 import BeautifulSoup
import json
import threading
import http.cookiejar as cookielib
import mechanize
import re

class Reports(threading.Thread):
    def __init__(self, email, pw, target):
        threading.Thread.__init__(self)
        self.email = email
        self.pw = pw
        self.tg = target

    def run(self):
        try:
            br = mechanize.Browser()
            url = "https://mbasic.facebook.com"

            # Configure browser settings
            br.set_handle_equiv(True)
            br.set_handle_referer(True)
            br.set_handle_robots(False)
            br.set_cookiejar(cookielib.LWPCookieJar())
            br.addheaders = [("User-Agent", "Mozilla/5.0 (Linux; Android 10; Mobile) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36")]

            # Login to Facebook
            br.open(url)
            br.select_form(action=re.compile(r'/login/'))
            br.form["email"] = self.email
            br.form["pass"] = self.pw
            br.submit()

            # Check if login was successful
            if "login" in br.geturl():
                print("[-] Login failed. Check credentials.")
                return

            # Navigate to target profile
            br.open(f"https://mbasic.facebook.com/{self.tg}")
            soup = BeautifulSoup(br.response().read(), 'html.parser')

            # Find the report link
            report_link = None
            for link in soup.find_all('a', href=True):
                if '/report/' in link['href']:
                    report_link = 'https://mbasic.facebook.com' + link['href']
                    break

            if not report_link:
                print("[-] Report link not found.")
                return

            # Access the report page
            br.open(report_link)
            soup = BeautifulSoup(br.response().read(), 'html.parser')

            # Select the 'Pretending to be someone else' option
            form = None
            for f in br.forms():
                if 'report/profile' in f.action:
                    form = f
                    break
            if not form:
                print("[-] Report form not found.")
                return
            br.form = form
            br.form.set_all_readonly(False)
            br.form['report_type'] = ['3']  # Pretending to be someone
            br.submit()

            # Confirm report type
            soup = BeautifulSoup(br.response().read(), 'html.parser')
            form = soup.find('form', action=lambda x: x and 'confirm' in x)
            if not form:
                print("[-] Confirmation form not found.")
                return
            form_action = form['action']
            br.open(f'https://mbasic.facebook.com{form_action}')
            
            # Final confirmation
            br.select_form(nr=0)
            br.submit()

            # Check for success
            response = br.response().read()
            if b'id="objects_container"' in response and b'Thanks' in response:
                print("[+] Report submitted successfully.")
            else:
                print("[-] Report submission failed. Response saved for debugging.")
                with open("debug.html", "wb") as f:
                    f.write(response)
        except Exception as e:
            print(f"[!] Error: {str(e)}")
