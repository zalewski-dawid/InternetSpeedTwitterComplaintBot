from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import tweepy
from requests_oauthlib import OAuth1Session
import json

class Bot:
    def __init__(self,consumer_key:str,consumer_secret:str,access_token:str,access_token_secret:str,client_id:str):
        self.download=150
        self.upload=100
        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(options=self.chrome_options)

        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.access_token = access_token
        self.access_token_secret = access_token_secret
        self.client_id=client_id








    def get_internet_speed(self):
        self.driver.get("https://www.speedtest.net/")
        element=self.driver.find_element(By.XPATH,value='//*[@id="container"]/div/div[3]/div/div/div/div[2]/div[3]/div[1]/a')
        time.sleep(4)
        element.click()
        time.sleep(45)


        try:
            speedtest_download=self.driver.find_element(By.XPATH,value='//*[@id="container"]/div/div[3]/div/div/div/div[2]/div[3]/div[3]/div/div[3]/div/div/div[2]/div[1]/div[1]/div/div[2]/span')
            speedtest_download=float(speedtest_download.text)


            speedtest_upload=self.driver.find_element(By.XPATH,value='//*[@id="container"]/div/div[3]/div/div/div/div[2]/div[3]/div[3]/div/div[3]/div/div/div[2]/div[1]/div[2]/div/div[2]/span')
            speedtest_upload=float(speedtest_upload.text)

            internet_provider=self.driver.find_element(By.XPATH,value='//*[@id="container"]/div/div[3]/div/div/div/div[2]/div[3]/div[3]/div/div[3]/div/div/div[2]/div[4]/div/div/div[1]/div[3]/div[2]')
            internet_provider=internet_provider.text
        except Exception as e:
            #if internet connection is slower wait for another 15 sec and try to read data again
            time.sleep(15)
            try:
                speedtest_download = self.driver.find_element(By.XPATH,
                                                              value='//*[@id="container"]/div/div[3]/div/div/div/div[2]/div[3]/div[3]/div/div[3]/div/div/div[2]/div[1]/div[1]/div/div[2]/span')
                speedtest_download = float(speedtest_download.text)

                speedtest_upload = self.driver.find_element(By.XPATH,
                                                            value='//*[@id="container"]/div/div[3]/div/div/div/div[2]/div[3]/div[3]/div/div[3]/div/div/div[2]/div[1]/div[2]/div/div[2]/span')
                speedtest_upload = float(speedtest_upload.text)

                internet_provider = self.driver.find_element(By.XPATH,
                                                             value='//*[@id="container"]/div/div[3]/div/div/div/div[2]/div[3]/div[3]/div/div[3]/div/div/div[2]/div[4]/div/div/div[1]/div[3]/div[2]')
                internet_provider = internet_provider.text

            except Exception as r:
                time.sleep(15)
                speedtest_download = self.driver.find_element(By.XPATH,
                                                              value='//*[@id="container"]/div/div[3]/div/div/div/div[2]/div[3]/div[3]/div/div[3]/div/div/div[2]/div[1]/div[1]/div/div[2]/span')
                speedtest_download = float(speedtest_download.text)

                speedtest_upload = self.driver.find_element(By.XPATH,
                                                            value='//*[@id="container"]/div/div[3]/div/div/div/div[2]/div[3]/div[3]/div/div[3]/div/div/div[2]/div[1]/div[2]/div/div[2]/span')
                speedtest_upload = float(speedtest_upload.text)

                internet_provider = self.driver.find_element(By.XPATH,
                                                             value='//*[@id="container"]/div/div[3]/div/div/div/div[2]/div[3]/div[3]/div/div[3]/div/div/div[2]/div[4]/div/div/div[1]/div[3]/div[2]')
                internet_provider = internet_provider.text


        #check with declared download and upload

        if speedtest_download < self.download or speedtest_upload < self.upload:

            self.tweet_at_provider(speedtest_download,speedtest_upload,internet_provider)







    def tweet_at_provider(self,speedtest_download,speedtest_upload,internet_provider):
        global fetch_response
        self.driver.quit()
        print("Tweeting...")
        print(f"download speed: {speedtest_download}")
        print(f"upload speed: {speedtest_upload}")
        print(f"internet_provider {internet_provider}")


        payload={"text":f"HEY {internet_provider}. WHAT IS WRONG WITH MY INTERNET??? DOWNLOAD SPEED: {speedtest_download} Mb/s UPLOAD SPEED: {speedtest_upload} Mb/s. DECLARED DOWNLOAD SPEED: {self.download} Mb/s UPLOAD SPEED: {self.upload} Mb/s."}
        request_token_url="https://api.twitter.com/oauth/request_token?oauth_callback=oob&x_auth_access_type=write"
        oauth = OAuth1Session(self.consumer_key, client_secret=self.consumer_secret)

        try:
            fetch_response = oauth.fetch_request_token(request_token_url)
        except ValueError:
            print(
                "There may have been an issue with the consumer_key or consumer_secret you entered "
            )

        resource_owner_key = fetch_response.get("oauth_token")
        resource_owner_secret = fetch_response.get("oauth_token_secret")
        print("Got OAuth token: %s" % resource_owner_key)

        # Get authorization
        base_authorization_url = "https://api.twitter.com/oauth/authorize"
        authorization_url = oauth.authorization_url(base_authorization_url)
        print("Please go here and authorize: %s" % authorization_url)
        verifier = input("Paste the PIN here: ")

        # Get the access token
        access_token_url = "https://api.twitter.com/oauth/access_token"
        oauth = OAuth1Session(
            self.consumer_key,
            client_secret=self.consumer_secret,
            resource_owner_key=resource_owner_key,
            resource_owner_secret=resource_owner_secret,
            verifier=verifier,
        )
        oauth_tokens = oauth.fetch_access_token(access_token_url)

        access_token = oauth_tokens["oauth_token"]
        access_token_secret = oauth_tokens["oauth_token_secret"]

        # Make the request
        oauth = OAuth1Session(
            self.consumer_key,
            client_secret=self.consumer_secret,
            resource_owner_key=access_token,
            resource_owner_secret=access_token_secret,
        )

        # Making the request
        response = oauth.post(
            "https://api.twitter.com/2/tweets",
            json=payload,
        )

        if response.status_code != 201:
            raise Exception(
                "Request returned an error: {} {}".format(response.status_code, response.text)
            )

        print("Response code: {}".format(response.status_code))

        # Saving the response as JSON
        json_response = response.json()
        print(json.dumps(json_response, indent=4, sort_keys=True))


        print("TWEET HAS BEEN SENT SUCCESSFULLY!")



