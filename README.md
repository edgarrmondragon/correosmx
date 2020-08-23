# Serveless Tracking Status Notifications

## Environment Variables

| Variable           | Description                                                                         |
|:------------------:|:-----------------------------------------------------------------------------------:|
| `EMAIL_TO`         | Email address to send the info to                                                   |
| `EMAIL_FROM`       | Email address to send the info from                                                 |
| `GUIA`             | Tracking ID of the package                                                          |
| `SENDGRID_API_KEY` | You can read more [here][sendgrid]. You can send 100 emails/day with a free account |
| `PERIODO`          | Year (default `2020`)                                                               |

## Installation

Requires installation of npm packages

```shell
npm install
```

## Deploy

This project uses the Serverless Framework to manage the function and its upstream resources:

```shell
serverless deploy
```

Or if you put your environment variables in a `.env` file:

```shell
env $(cat .env | xargs) serverless deploy
```

### Notes

- If you are using an [AWS named profile][profiles], you might need to do the following before deploying:

    ```shell
    export AWS_PROFILE=myprofile
    export AWS_SDK_LOAD_CONFIG=1
    ```

[sendgrid]: https://sendgrid.com/docs/ui/account-and-settings/api-keys/
[profiles]: https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-profiles.html
