# 🤖 Contessa: Contest Alert Bot

[![Run Check](https://img.shields.io/github/actions/workflow/status/Sarthak-Sahu-1409/Contessa_Bot/contest-alert.yaml?label=Run%20Check&style=flat-square)](https://github.com/Sarthak-Sahu-1409/Contessa_Bot/actions)

A serverless bot using GitHub Actions to send Telegram alerts for upcoming competitive programming contests from `clist.by`.

The workflow runs every two hours and notifies you of contests starting within that window.

### Quick Setup

1.  Fork this repository.
2.  Create a Telegram Bot (`@BotFather`) to get a `TELEGRAM_TOKEN`.
3.  Get your `TELEGRAM_CHAT_ID` from a bot like `@userinfobot`.
4.  Add your `CLIST_USER`, `CLIST_KEY`, `TELEGRAM_TOKEN`, and `TELEGRAM_CHAT_ID` as repository secrets.
