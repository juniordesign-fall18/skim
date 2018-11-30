# Skim
Skim is a course data visualization tool designed for the University of Alabama in Huntsville. Skim allows administrators to compare class enrollment data accross years and allows administrators to view enrollment data of different classes on the same graph. Skim is designed to be used as a tool to assist administrators with defining current course max capacities. 

## Release Notes for Version 1.0
### New Software Features:
 - Population of course data from Fall 2015 to Fall 2018
 - Can view max and current enrollment trendlines for a course
	 - Hovering feature on graph to see semesterly detail
 - Search bar for course numbers
 - Support for multiple course trendline visualization
	 - Toggle trendline appearance for each course
 - Reset functionality for clearing graph

### Known Bugs and Defects:
- Accessibility compliance for graph colors
- Auto-refresh of data

## Installation
Skim is built as a webpage in flask. We provide instructions for running and testing the application. If you are trying to deploy this to an actual webpage, we reccomend following the deployment reccomendations provided in the [flask documentation](https://explore-flask.readthedocs.io/en/latest/deployment.html)

### Dependencies
-  [python 3.4.9](https://www.python.org/downloads/)
-  [flask](https://github.com/pallets/flask)
-  [requests](https://github.com/requests/requests)
-  [Pyrebase](https://github.com/thisbejim/Pyrebase)
-  [pyenv](https://github.com/pyenv/pyenv)

Flask, Requests, and Pyrebase can all be installed using pip as well:
`pip install flask requests pyrebase`

### Getting Started
1. Install dependencies
2. Clone this repository
3. Run `run_win.sh` if on windows, or `sh run_mac.sh` if on mac/linux. The purpose of these shell scripts is to set your python environment and flask environment variables, and then actually start the server on your local machine. These should NOT be used for actual deployment.

Running the project on Linux has not been tested, but there is no clear reason as to why it wouldn't (should be the same as mac)
