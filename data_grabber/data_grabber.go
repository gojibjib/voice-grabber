package main

import (
	"encoding/csv"
	"encoding/json"
	"github.com/gojibjib/gopeana"
	"io/ioutil"
	"log"
	"os"
	"strconv"
	"strings"
)

type Bird struct {
	Name       string   `json:"name"`
	Genus      string   `json:"genus"`
	Species    string   `json:"species"`
	Url        []string `json:"url"`
	VoiceFiles int      `json:"voice_files"`
}

func checkErr(err error) {
	if err != nil {
		log.Fatalln(err)
	}
}

func extractURL(s string) string {
	query := strings.SplitAfter(strings.TrimPrefix(s, "https://www.europeana.eu/api/v2/thumbnail-by-url.json?uri="), "mp3")[0]

	//query = url.QueryEscape(query)
	query = strings.Replace(strings.Replace(query, "%2F", "/", -1), "%3A", ":", -1)
	return query
}

func main() {
	// API stuff
	apiKey := os.Getenv("APIKEY")
	secretKey := os.Getenv("SECRETKEY")
	birdMap := make(map[string]*Bird)
	currCount := 0

	// CSV stuff
	var records [][]string
	csvFile := "birds.csv"
	records = append(records, []string{"name", "genus", "species", "voice_files"})

	// JSON stuff
	jsonFile := "birds.json"

	client := gopeana.NewClient(apiKey, secretKey)
	cursor := ""

	// Getting all necessary information into a slice
	for {
		req, err := gopeana.NewCursorSearchRequest(client, "open", "standard", cursor)
		checkErr(err)

		resp, err := gopeana.Get(req, "tierstimmenarchiv")
		checkErr(err)

		currCount += resp.ItemsCount
		log.Printf("Fetched %d/%d", currCount, resp.TotalResults)

		for _, item := range resp.Items {
			if item.Title[0] == "" {
				log.Fatalf("No title provided for %s", item.ID)
			}

			nameList := strings.Split(item.Title[0], " ")[:2]
			name := strings.Join(nameList, " ")

			// If bird hasn't appeared yet, create it as struct
			if birdMap[name] == nil {
				genus := nameList[0]
				species := nameList[1]
				birdMap[name] = &Bird{
					Name:       name,
					Genus:      genus,
					Species:    species,
					Url:        nil,
					VoiceFiles: 0,
				}
			}

			// Extract all voice URLs for a specific bird
			var urlSlice []string
			for _, u := range item.Preview {
				urlSlice = append(urlSlice, extractURL(u))
				birdMap[name].VoiceFiles += 1
			}
			birdMap[name].Url = append(birdMap[name].Url, urlSlice...)
		}

		if resp.NextCursor == "" {
			break
		}

		cursor = resp.NextCursor
	}

	// Create rows for birds.csv
	for _, r := range birdMap {
		records = append(records, []string{r.Name, r.Genus, r.Species, strconv.Itoa(r.VoiceFiles)})
	}

	// Save to .csv
	csvOut, err := os.Create(csvFile)
	checkErr(err)
	defer csvOut.Close()

	writer := csv.NewWriter(csvOut)
	writer.Comma = '|'
	writer.WriteAll(records)
	checkErr(writer.Error())

	// Save to .json
	birdJson, err := json.Marshal(birdMap)
	checkErr(err)
	err = ioutil.WriteFile(jsonFile, birdJson, 0644)
	checkErr(err)
}
