# netgear-automator

Simple utility that logs in to my Netgear router to either enable or disable the
blocking of configured services.

It runs on linux and you can schedule `run.sh` using cron.

Install by running the `install.sh` script.

Set credentials as environment variables: `NETGEAR_USERNAME` and `NETGEAR_PASSWORD`

Running the util.

```bash
# to enable blocking of services
./run.sh enable

# to disable blocking of services
./run.sh disable
```
