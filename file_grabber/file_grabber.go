package main

import (
	"encoding/json"
	"fmt"
	"io"
	"io/ioutil"
	"log"
	"net/http"
	"os"
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

func mkdir(name string) {
	_, err := os.Stat(name)
	if os.IsNotExist(err) {
		err = os.Mkdir(name, 0755)
		checkErr(err)
	}
}

func downloadFile(query, filepath string) int {
	var code int

	// Get the data
	resp, err := http.Get(query)
	checkErr(err)
	defer resp.Body.Close()

	// Check status code
	code = resp.StatusCode
	if code != http.StatusOK {
		log.Printf("Bad status: %d", resp.StatusCode)
		return code
	}

	// Creating the file
	out, err := os.Create(filepath)
	checkErr(err)
	defer out.Close()

	// Write to file
	_, err = io.Copy(out, resp.Body)
	checkErr(err)

	return code
}

func main() {
	var iBird int
	birdMap := make(map[string]Bird)
	notFound := make(map[string][]string)
	jsonFilename := "birds.json"

	// Create ./files folder
	mkdir("files")

	jsonFile, err := ioutil.ReadFile(jsonFilename)
	checkErr(err)

	err = json.Unmarshal(jsonFile, &birdMap)
	checkErr(err)

	nBird := len(birdMap)

	for _, bird := range birdMap {
		// Create ./files/%GENUS_%SPECIES folder
		folderName := fmt.Sprintf("%s/%s_%s", "files", bird.Genus, bird.Species)
		mkdir(folderName)

		if iBird%150 == 0 {
			fmt.Printf("-- Downloading files for %s (%d/%d) into %s\n", bird.Name, iBird+1, nBird, folderName)
		}

		//nURL := len(bird.Url)
		for iURL, u := range bird.Url {
			fileName := fmt.Sprintf("%s_%s_%d.mp3", bird.Genus, bird.Species, iURL+1)
			path := fmt.Sprintf("%s/%s", folderName, fileName)
			//fmt.Printf("+ (%d/%d) Downloading %s from %s as %s\n", iURL+1, nURL, fileName, u, path)
			code := downloadFile(u, path)
			if code == 404 {

			}
			notFound[bird.Name] = append(notFound[bird.Name], u)
		}
		iBird++
	}

	// Export notFound as JSON
	nfJSON, err := json.Marshal(notFound)
	checkErr(err)
	err = ioutil.WriteFile("not_found.json", nfJSON, 0644)
	checkErr(err)
}
