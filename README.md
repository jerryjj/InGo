WARNING: Still under heavy development, this notification will be removed when the code is somewhat stable :WARNING

# InGo will be free and open multi purpose python framework

InGo will try to do it's best not to define how you should write your projects,
but to provide a small and efficient core for multiple different needs.

Main reason for building this project is to fasten my own development on all the
different projects I work on.

## Main points

* Core will be small
* Features will be installed as extensions and plugins
* Helper packages fasten development in specific tasks

## Where are we now

* Small core

### Extensions

* InGo.web
  Basic set of common utils needed in web projects
  
* InGo.ext.cherrypy
  Depends: InGo.web
  Can be used as projects "server"

* InGo.ext.templating
  Common templating related methods

* InGo.ext.templating.genshi
  Depends: InGo.ext.templating
  Genshi template engine support

## Packages

There will be few stock packages which will fasten development in different projects

### Web development

* Package: InGo.package.website
  Depends on basic packages which are needed for web development including
  InGo.ext.cherrypy, InGo.ext.templating.genshi and their dependencies.
  Will also install paster create template for scaffolding (paster create -t ingo_website)
  
### Messaging related


## Extensions planned
Some of the planned extensions are

* database.mongodb
* database.redis
* database.sqlalchemy
* authentication.*
* authorization.*
* messaging.amqp
* messaging.xmpp
* caching.memcached
* caching.redis
* background.cron
* publisher.timed