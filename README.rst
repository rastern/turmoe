.. _Django https://www.djangoproject.com/
.. _vmt-connect https://pypi.org/project/vmtconnect/

======================
Turbonomic Mock Engine
======================

Introduction
============

Installation
============

Requirements
------------

Turmoe utilizes the `Django`_ framework for mocking API calls, and handling basic
HTTP communications. Django and PyYAML are required, along with their dependencies.
A pip requirements file is included in the repository, and can be used to quickly
install all requirements as follows:

.. code-block:: bash

  # change /dev/ to /master/ to snag the latest from the master branch instead
  curl -O https://raw.githubusercontent.com/rastern/turmoe/dev/requirements.txt

  pip install -r requirements.txt


Django Application
------------------

The simplest and most direct way to install Turmoe is to clone the git repository
directly to your local system.

.. code-block:: bash

  git clone https://github.com/rastern/turmoe.git

You can also clone only the latest dev or master branch commits, if you do not
wish to install the entire repository.

.. code-block:: bash

  git clone -branch dev -depth=1 https://github.com/rastern/turmoe.git

Alternatively the source for a branch can be downloaded as a compressed archive

* Master: https://github.com/rastern/turmoe/archive/master.zip
* Dev: https://github.com/rastern/turmoe/archive/dev.zip


Running Turmoe
==============

Turmoe uses the `Django`_ framework, which comes
packaged with a development webserver that runs locally. There is no reason to
install Turmoe into a product webserver, and the Django dev server should be used.
A startup script, **start.sh**, is provided that accepts an optional port number.
If no port number is provided, the default 8000 is used.

.. code-block:: bash

  ./start.sh

You should then see the following:

.. code-block:: bash

 Loading namespace config 'namespaces/classic/namespace.json'
  Removing temporary tables from previous run
  Operations to perform:
    Unapply all migrations: engine
  Running migrations:
    Rendering model states... DONE
    Unapplying engine.0001_initial... OK

  Initializing API engine database
  Operations to perform:
    Apply all migrations: engine
  Running migrations:
    Applying engine.0001_initial... OK

  Disabling auto-reloader
  Performing system checks...

  System check identified no issues (0 silenced).
  June 29, 2020 - 13:34:03
  Django version 3.0.6, using settings 'turmoe.settings'
  Starting development server at http://127.0.0.1:8000/
  Quit the server with CONTROL-C.

With this, the server is now running. To stop it, press Ctrl-C at the console to
force the server to halt.


Configuration
=============

The main Django settings file is located at turmoe/settings.py relative to the
root project folder. In general, Django settings should not be modified. Turmoe
specific settings are located at the bottom of the file, and include:

* **ENGINE_BASE_DIR** : The base path for the namespace repository
* **ENGINE_NAMESPACE** : The current namespace to serve
* **ENGINE_MESSAGE_DEBUG** : Extra debug information for troubleshooting messages
* **ENGINE_API_BASE_PATH** : API base path to prepend to serve from
* **ENGINE_API_DEFAULT_CONTENT_TYPE** : Default API content-type to serve
* **ENGINE_API_DYNAMIC_URLS** : Enable dynamic URL rewriting, useful for developing namespaces


Namespaces
==========

Collections of mocking messages are organized into groups called namespaces.
Namespaces do not stack or inherit from each other, and all desired messages
(requests & responses) must be created anew. When using Turmoe with `vmt-connect`_,
a minimum namespace must include a version message, as required by vmt-connect
to establish a session.

Each namespace may override the base configuration individually, to enable per
namespace configurations. This is especially important for mocking multiple versions
of APIs with distinct base paths, or message variations. To set namespace specific
configuration settings, Turmoe looks for a file called **namespace.json** in the
root folder of the namespace.


Message Definition
==================

Each mocked API call comprises a request, sent by the client, and a response,
sent by the server. Collectively these request-response pairs are called messages.
Multiple messages, such as a chain of paged results, are not treated distinctly
as successive calls to fetch additional pages require unique requests to the
server. In cases where successive calls to the same endpoint need to return unique
results based on some internal state of the server, Turmoe supports setting and
comparing state variables, thus you can simulate complex environments that change
over time and in response to specific calls, such as updates, deletions, etc.

Message files are YAML documents containing a **request** and a **response**
block. Each block comprises a set of attributes, of which most are optional.
Each request is treated as an input filter. Turmoe searches for the first request
block that matches the currently received request, and when found, sends the
adjoining response to the client. This includes checking required state on the
request end (if specified), and setting state when sending the response, if
defined. There is no technical limitation that prevents having multiple messages
that define the same request - doing so will result in potentially unpredictable
responses, as Turmoe will serve the first message that matches, which is determined
by the OS dependent directory listing capabilities that are not guaranteed to be
idempotent. Thus care should be exercised to ensure your requests are sufficiently
unique.

Requests:
^^^^^^^^^
* **method** : Request REST method (required)
* **headers** : List of input headers (e.g. for cursors or pagination)
* **path** : API path of the request, if not using a full directory tree representation
* **parameters** : URL parameters
* **state** : Required sever state
* **body** : Request body to require (e.g. for form input, be sure to set required headers)

Response:
^^^^^^^^^
* **headers** : List of response headers
* **state** : Response state to set on the sever
* **status_code** : HTTP response status code
* **body** : Response body to send
