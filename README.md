# Skim

A Course Enrollment Data Visualization Tool for UAH

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

## Dependencies

-  [Python 3.4.9](https://www.python.org/downloads/)
-  [Flask](https://github.com/pallets/flask)
-  [Requests](https://github.com/requests/requests)
-  [Pyrebase](https://github.com/thisbejim/Pyrebase)

For the development setup, add the following line to your .profile:
`eval "$(pyenv init -)" `

## Getting Started
1. Clone this repository
2. Run `run_win.sh` if on windows, or `sh run_mac.sh` if on mac