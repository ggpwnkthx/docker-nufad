# Purpose
(N)ginx, (U)wsgi, and (F)lask, on (A)lpine in a (D)ocker container

NUFAD is a dockerized web service designed to provide a modular API writen in Python for enterprise use.

# Modularity
NUFAD, at its very core, is designed to be modular. In fact, the modules that make up NUFAD's core are the configuration, logging, api, authentication, and permissions modules.

## Core:Configuration
This module sets up SQLAlchmey and database bindings. To use the built in SQLite database, import it into your module's script with the following line:
```from core.configuration.sql import db```
Check out the Packages:AuthenticationLocal module (specifically setup.py) as an example of how the Core:Configuration module can be used.
## Core:Logging
This module provide a simple mechanism to log events to the console as well as to log files. 
```
from core.logging.api import info warning error
info("This text will be log for informational purposes.")
warning("This text will be log for warning purposes.")
error("This text will be log for error purposes.")
```
## Core:Api
Arguably this is the heart of NGINX, and even it is design to be modular, allowing for separate routing to different API versions.
### v1
This version is currently the only version available to NUFAD. It is accessible via HTTPS only, and from the route "/api/v1".
#### Requests
Only GET and POST requests are supported. GET requests will always provide a list of methods and functions that the current sessions is allowed to call. POST requests will be parsed and executed if the current session has permission.
POST requests need to have a BODY that defines an "action". The "action" needs to specify the "module" that will be used, a "function" that module provides, and (if required by that function) "arguments" that function may need.
With APIv1, we strictly use JSON in the BODY of the POST request.
```{
	"action" : { 
		"module" : "MODULE.PATH", 
		"function" : "PYTHON_FUNCTION", 
		"arguments" : { 
			"NAMED_ARGUMENT_1" : "ARGUMENT_VALUE", 
			"NAMED_ARGUMENT_2" : "ANOTHER_ARGUMENT_VALUE"
		}
	}
}```
You can also request a queue of actions:
```{
	"actions" : [
		{ 
			"module" : "MODULE.PATH", 
			"function" : "PYTHON_FUNCTION", 
			"arguments" : { 
				"NAMED_ARGUMENT_1" : "ARGUMENT_VALUE", 
				"NAMED_ARGUMENT_2" : "ANOTHER_ARGUMENT_VALUE"
			}
		},
		{ 
			"module" : "MODULE_2.PATH", 
			"function" : "DIFFERENT_PYTHON_FUNCTION", 
			"arguments" : { 
				"NAMED_ARGUMENT_1" : "ARGUMENT_VALUE", 
				"NAMED_ARGUMENT_2" : "ANOTHER_ARGUMENT_VALUE"
			}
		},
		
	]
}```
#### Sessions
Flask is heavily leaveraged for session management. 
## Core:Authentication
This module is designed to be extended. It should be used to manage other authentication modules. It does NOT do any actual authenticating. It just sets up sessions if/when a separate authenticating module says it's OK to do so.
### API
#### Login
To login and create a session, you'll need a POST request with a BODY similiar to the following:
```{
	"action" : { 
		"module" : "core.authentication", 
		"function" : "login", 
		"arguments" : { 
			"method" : "packages.authentication_local", 
			"args" : { 
				"username":"nufad",
				"password":"nufad" 
			}
		}
	}
}```
In this case, we are using the "packages.authentication_local" module to process the authentication based on the provided "username" and "password" arguments.