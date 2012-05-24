★ xdapy ★
===========

*A Python database wrapper.*

☞ [Documentation on github] (http://debilski.github.com/xdapy/)

Prerequisites
-------------

* Python 2.6 / 2.7
* SQLAlchemy
* psycopg2 (Python–PostgreSQL Database Adapter)
* A postgresql database

Information concerning the Compass CSS interface.
-------------------------------------------------

The CSS files are generated using the Compass framework [1].  This framework
takes files in the SCSS format and creates plain CSS files which can be read by
all browsers. The advantage of Compass is that it allows for the nesting of
style declarations and defines easy-to-use mixins which can be used to apply
the same style properties to unrelated classes.

In order to use the Compass framework, one has to use ruby bundle [2].

Updating the CSS is done using

    > compass compile

Note that we aim to put both SCSS and CSS files under source control. This may
be a hurdle for the CSS developer as it may result in unneeded conflicts every
now and then but on the other hand it means that users do never need to install
Compass unless they want to change the CSS.

[1]: http://compass-style.org/
[2]: http://gembundler.com/
