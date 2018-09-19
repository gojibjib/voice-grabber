# [voice-grabber](https://github.com/gojibjib/voice-grabber)
This repo is a collection of scripts to download the dataset necessary to train the [jibjib-model](https://github.com/gojibjib/jibjib-model)

## Repo layout
The complete list of JibJib repos is:

- [jibjib](https://github.com/gojibjib/jibjib): Our Android app. Records sounds and looks fantastic.
- [deploy](https://github.com/gojibjib/deploy): Instructions to deploy the JibJib stack.
- [jibjib-model](https://github.com/gojibjib/jibjib-model): Code for training the machine learning model for bird classification
- [jibjib-api](https://github.com/gojibjib/jibjib-api): Main API to receive database requests & audio files.
- [jibjib-data](https://github.com/gojibjib/jibjib-data): A MongoDB instance holding information about detectable birds.
- [jibjib-query](https://github.com/gojibjib/jibjib-query): A thin Python Flask API that handles communication with the [TensorFlow Serving](https://www.tensorflow.org/serving/) instance.
- [gopeana](https://github.com/gojibjib/gopeana): A API client for [Europeana](https://europeana.eu), written in Go.
- [voice-grabber](https://github.com/gojibjib/voice-grabber): A collection of scripts to construct the dataset required for model training

## Scripts
In the top level of this repo, there are several helper scripts to create/change JSON and CSV files, as well as `converter.py` to convert audio files from `mp3` to `wav`.

### [data_grabber/](https://github.com/gojibjib/voice-grabber/tree/master/data_grabber)
This Go script uses [gopeana](https://github.com/gojibjib/gopeana) to populate both a JSON and CSV file with information about the on Europeana published bird voices from the [Tierstimmenarchiv](www.tierstimmenarchiv.de) ([open dataset](https://www.europeana.eu/portal/de/search?f[REUSABILITY][]=open&q=tierstimmenarchiv) of the [Museum für Naturkunde Berlin](https://www.museumfuernaturkunde.berlin/))

### [file_grabber/](https://github.com/gojibjib/voice-grabber/tree/master/file_grabber)
This Go script uses the output of [data_grabber/](https://github.com/gojibjib/voice-grabber/tree/master/data_grabber) to follow the links provided on Europeana and download the audio files.

### [wiki_grabber/](https://github.com/gojibjib/voice-grabber/tree/master/wiki_grabber)
This Python script takes input from a CSV file and uses the Wikipedia API to extract summaries about birds, then saves it in a seperate CSV.

### [xeno_grabber/](https://github.com/gojibjib/voice-grabber/tree/master/xeno_grabber)
This is a collection of scripts to:

- clean the files directory (in our case, in order to bring down the total number of classes, birds with a German Wikipedia entry were used.)
- nicely crawl [Xeno Canto](www.xeno-canto.org) for audio files of birds
- download the audio files from Xeno Canto
