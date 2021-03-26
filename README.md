# CurlForACurl
An automatic pre-registration script for IMLeague events.

## Motivation
This project was created because I was tired of not being able to secure a spot for a yoga class at my college gym. The project's name is a slight play on words referring to the curl Linux command-line tool and curling weights.
 
## Screenshot
![Screen Shot 2021-03-25 at 11 04 47 PM](https://user-images.githubusercontent.com/21346818/112571538-a49d3180-8dbe-11eb-8d58-cdbb1ece38dd.png)

## Features
- Multi-user support
- Event ID sanitization
- Guided Setup Process

## Installation
Run `./curlForACurl` to begin the guided setup process.

### Crontab Script
To automatically run the program every day at 6 in the morning, add this line to your crontab file.
```0 6 * * * cd PROJECT_DIR && python3 autoRunner.py > PROJECT_DIR/log.txt```
## Usage
Run `./curlForACurl` and input the desired user's email address.

## Contribute
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
MIT © [Griffith Baker]()
