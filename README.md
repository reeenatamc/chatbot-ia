# chatbot-ia

**CantaClaro** answers questions about what is happening in Loja, Ecuador —
concerts, fairs, public events — in the way someone from Loja would answer them.

## What it does

You ask in plain Spanish. Google Gemini interprets the question, the app
searches its own event database, and the answer comes back in local slang rather
than in neutral corporate Spanish. That last part is the point: a tourism bot
that sounds like a press release is a bot nobody uses twice.

Events are managed through the Django admin, so the people who know what is on
this weekend can update it without touching the model or the code.

## Stack

Django 5 · Google Gemini · django-unfold for the admin.

## Running it

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Set your Gemini API key in the environment first. The chat lives at `/`, the
event admin at `/admin/`.

## Licence
MIT
