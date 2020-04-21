# Serveless Tracking Status Notifications

## Variables

### Required

- `EMAIL_TO`
- `EMAIL_FROM`
- `GUIA`
- `SENDGRID_API_KEY`

### Optional

- `PERIODO` (default 2020)

## Deploy

```shell
export AWS_PROFILE=myprofile
export AWS_SDK_LOAD_CONFIG=1
chamber exec personal -- serverless invoke --function send_status
```
