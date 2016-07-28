# twilio-c9-bootstrap
###### Jumpstart your first Twilio app using Python and Cloud9!

twilio-c9-bootstrap is designed to make setting up your first Twilio app a breeze. Here's a walkthrough of how to get one up in no time.

1. [Set up a Twilio account](https://www.twilio.com/try-twilio).
  - Make note of your Account SID & Auth Token, which can be found under your [Account Settings](https://www.twilio.com/user/account/settings).
1. [Buy a phone number](https://www.twilio.com/user/account/phone-numbers/search).
  - Under your [list of incoming phone numbers](https://www.twilio.com/user/account/phone-numbers/incoming), click on your new Twilio number and make note of its SID.
1. [Set up a Cloud9 account](https://c9.io/web/sign-up/free) and [create a new workspace](https://c9.io/new).
  - Under `Clone from Git or Mercurial URL` enter `https://github.com/perfectlynormalbeast/twilio-c9-bootstrap`
  - Under `Hosted workspace` select `Public`
  - Under `Choose a template` select `Python`
1. Set up your starter code.
  - In your newly created workspace, click on the terminal window (bottom pane).
  - Type `make install` and return.
  - Enter your credentials from steps 1 and 2 when prompted.
  - Type `python run.py` and enter to run your server.

You're all set to start developing your first Twilio app.

##### Additional `make` options
- `make` - Installs, configures and starts your server
- `make install` - Installs and configures your server
- `make configure` - Reconfigures your server
- `make serve` - Starts your server
- `make clean` - Uninstalls your server
