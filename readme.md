# 2FA on Slack

2FA on Slack allows you to automatically create one-time-passwords for online services you're using (such as Gmail, Mailchimp and Github), directly on Slack using slash commands.

You can deploy this app to an App Engine instance on Google Cloud. Tokens for each account you use will be stored on Google Cloud Firestore.

## Installation

1. Create a virtual environment with Python 3, activate it, then install the packages in requirements.txt

```bash
virtualenv env
source env/bin/activate
pip install -r requirements.txt
```

2. Create an app.yaml for App Engine deployment, and add your Slack app token as an environment variable.

```yaml
runtime: python37
instance_class: F1

env_variables:
  SLACK_TOKEN: 'XXXXXXXXXXXXXXXX'
```

3. Within your Google Cloud project, activate the Firestore API, create service account credentials, and add the `service-account.json` file generated in the root of your project.

4. Deploy the app to the Google Cloud App Engine.

```bash
gcloud app deploy
```

5. Retrieve the App Engine instance's URL (which should be output on console once the deployment is complete), and add it as a Request URL within your Slack app's slash settings page. The app will accept Slack requests on the `/slash` directory.

## Usage

To register a new token, you'll first need the TOTP URI generated during the 2FA set up process on your account. The URI will look something like this: `otpauth://totp/testaccount@us1.admin.mailchimp.com?secret=3N73THMLTABUN37Y`. You'll need the `secret` parameter on this URI.

Add the new token on Slack using the slash command: `/otp add [name] [secret]`.

![](https://media.giphy.com/media/QZaOsK883iJRWjhtyl/giphy.gif)

To generate a one-time-password simply type `/otp get [name]` on Slack.

![](https://media.giphy.com/media/UrQ7pAFZItv1gOzT78/giphy.gif)

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)



