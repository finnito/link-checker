## What is This?

This is a Python script that checks the HTTP status of every `<a>` element on a website using it's `sitemap.xml` and produces a report which is stored on your server and emailed to you (if enabled)!

Simply attach it to your crontab to run it on a regular basis and be aware of any dead links that need fixing!

Sound good?

<a href="https://www.buymeacoffee.com/FinnLeSueur" target="_blank">
    <img src="https://cdn.buymeacoffee.com/buttons/lato-orange.png" alt="Buy Me A Coffee" style="max-width: 150px; width: 150px !important; height: auto;"/>
</a>

## ✅ Getting Started

1. Clone the repo

```bash
cd ~/
git clone git@gitlab.com:Finnito/link-checker.git
cd link-checker
```

2. Install [pipenv](https://pypi.org/project/pipenv/)

```bash
sudo apt install pipenv
```

3. Install the project

```bash
pipenv install
```

4. Configure some settings

```bash
cp config.example config
nano config
```

```
[default]
sitemap_url     = http://localhost:1313/sitemap.xml     # The script only does XML sitemaps
email_log       = yes                                   # Set to "no" to disable email logs
to_email        = your@email.com                        # Ensure the domain meets your mail server requirements
from_email      = from@email.com                        # Who's getting the email reports?
email_subject   = Link Checker reports                  # Customise the subject in case you don't like it!
```

5. Test the script!

```bash
python3 -m pipenv run link-checker
```

6. Setup a [crontab](https://crontab.guru/), I prefer mine to run at 6am each Monday like so:

```
crontab -e

# Paste the following
0 6 * * 1 cd ~/link-checker/ && python3 -m pipenv run link-checker
```

## Extra for Experts (not really)

You can alternatively pass the sitemap URL as an argument to the script - this will override the `config` file allowing you to check multiple sites with the one script. It might look like this in your crontab:

```
0 6 * * 1 cd ~/link-checker/ && python3 -m pipenv run link-checker https://finn.lesueur.nz/sitemap.xml
5 6 * * 1 cd ~/link-checker/ && python3 -m pipenv run link-checker https://science.lesueur.nz/sitemap.xml
```