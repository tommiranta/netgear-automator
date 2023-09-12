# netgear-automator

Simple utility that logs in to my Netgear router to either enable or disable the
blocking of configured services.

It runs on linux and you can schedule `run.sh` using cron.

Install by running the `install.sh` script.

Add the `NETGEAR_USERNAME` and `NETGEAR_PASSWORD` variables to a `.env` file.

Running the util.

```bash
# to enable blocking of services
./run.sh enable

# to disable blocking of services
./run.sh disable
```

## Scheduling with crontab

Below example will run the script on schedule and write all outputs to a log file.

`0 17 * * 1,2,3,4,5 /home/user/netgear-automator/run.sh disable >> /home/user/netgear.log 2>&1`
