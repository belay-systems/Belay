# Security

Belay is foundation-stage research software. It places no orders and holds no
credentials. It is still built to handle money eventually, so reports are
welcome now.

## Reporting a vulnerability

Please report privately, not in a public Issue or pull request. On this
repository's GitHub page, open the **Security** tab and choose **Report a
vulnerability**. That opens a private advisory only the owners can read.

Say what you found, where (file and line, or the steps to reproduce it), and
what you think it allows. You will get a reply in the advisory thread.

## What counts

- Anything that could expose a secret, an account, or personal data.
- Anything that lets a pull request from a fork do more than read the code, for
  example through the continuous integration workflow.
- Anything that lets a stored artifact or a market data file be altered without
  its integrity check failing.
- Anything that lets a strategy reach a capital stage without passing the gates
  in `constitution/`.

An ordinary defect that is not a security problem belongs in an Issue.

## What never belongs in this repository

Credentials, tokens, session files, account identifiers, personal file paths,
email addresses, balances, positions or trade history. If you see any, report it
the same private way.
