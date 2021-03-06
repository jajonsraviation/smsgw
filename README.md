# SMSGW SMS management system
[![Circle CI](https://circleci.com/gh/VojtechBartos/smsgw/tree/master.svg?style=svg)](https://circleci.com/gh/VojtechBartos/smsgw/tree/master)

SMSGW is open source web-based SMS (Short Message Service) management system, it use gammu-smsd (part of gammu family) as SMS gateway engine to deliver and retrieve messages from your phone/modem.

**NOTICE: still in active development as part of the master thesis**

![SMSGW Dashboard](https://raw.githubusercontent.com/VojtechBartos/smsgw/master/docs/_static/images/screen-dashboard.png "SMSGW Dashboard")

## Requirements

- [docker](https://github.com/docker/docker) >= 1.9.0
- [docker-compose](https://github.com/docker/compose) >= 1.5.2
- for deployment and provisioning
  - [ansible](http://www.ansible.com/) >= 1.8.2
- for development
  - [node.js](https://nodejs.org/en/) >= 5.1.0
  - [gulp](https://www.npmjs.com/package/gulp) >= 3.9.0
    - `npm install -g gulp`

## Getting started

```sh
# cloning repository
git clone git@github.com:VojtechBartos/smsgw.git
cd smsgw

# creating .env file with environment variables and replacing placeholders
cp .env.sample .env
vim .env

# running app
make dev # for dev environment with container output
# OR
make # for production env in background
```

## Provisioning fresh new server

You need to have prepared fresh new machine with SSH access and IP address

```sh
# copy sample host file
cp provisioning/hosts.sample provisioning/hosts

# update host file with SSH user, IP address and domain/hostname of machine
vim provisioning/hosts

# copy sample vars file for SMSGW project
cp provisioning/groups_vars/smsgw/service.yml.sample provisioning/groups_vars/smsgw/service.yml

# update vars file for SMSGW project with your env variables for production,
# new DB and RabbitMQ will be created
vim provisioning/groups_vars/smsgw/service.yml

# run ansible provisioning which will prepare and start SMSGW project on your machine
make deploy

# open browser on hostname, if your DNS pointing to right machine you should
# see SMSGW sign in page
```

## Issues

- What if i am using VPS in VirtualBox?
  - Make sure that you have installed VirtualBox Quest Additions. [tutorial](http://en.ig.ma/notebook/2012/virtualbox-guest-additions-on-ubuntu-server)

- I am not able to see GSM modem in `/dev`
  - Follow this [tutorial](https://www.raspberrypi.org/forums/viewtopic.php?f=36&t=80925)

## TODO's

- Documentation
- Better tests coverage
- Make final JS bundle smaller
- Packages
  - upgrade `react-router`
  - upgrade `react-tagsinput`
- Functionality
  - ~~verifying passwords during change in settings and admin page~~
- DevOps
  - ~~write installation steps~~
  - replace `vojtechbartos/nginx` with https://github.com/jwilder/nginx-proxy
  - add flower monitoring
  - ~~build image on CircleCI and pushing to Docker Hub [via rarous](https://github.com/rarous/rarousnet/blob/master/circle.yml)~~
  - after success push to Docker Hub run ansible provisioning script to deploy and update server
