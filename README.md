# voice-grabber
This repo is a collection of scripts leveraging [gopeana](https://github.com/gojibjib/gopeana) to download the [CDV 2018 Ost](https://codingdavinci.de/events/ost/) dataset of [bird voices](https://www.europeana.eu/portal/de/search?f%5BREUSABILITY%5D%5B%5D=open&q=tierstimmenarchiv).

## Instructions
Get the repo

```
$ git clone https://gojibjib/voice-grabber
```

Set your API key and secret key as environment variables

```
$ export APIKEY=XXXXX
$ export SECRETKEY=YYYYY
```

Run `data_grabber.go` to extract the necessary URLs. This will also generate a `.csv` file with colums for `name`, `genus`, `species` and number of `voice_files`, as well as a `.json` file with the same information.

```
$ go run data_grabber/data_grabber.go
```

Run `file_grabber.go` to download the files. They will then be placed in the `files/` folder:

```
$ tree files/
.
├── Accipiter_brevipes
│   └── Accipiter_brevipes_1.mp3
├── Accipiter_castanilius
│   └── Accipiter_castanilius_1.mp3
├── Accipiter_gentilis
│   ├── Accipiter_gentilis_1.mp3
│   ├── Accipiter_gentilis_2.mp3
│   ├── Accipiter_gentilis_3.mp3
│   ├── Accipiter_gentilis_4.mp3
│   ├── Accipiter_gentilis_5.mp3
│   └── Accipiter_gentilis_6.mp3
# ...
```

## Stats
Key|Value
---|---
Unique birds|1189
Total number of bird voices|3843
avg(voices / bird)|3,23