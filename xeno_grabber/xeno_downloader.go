package main

import (
	"encoding/json"
	"fmt"
	"io"
	"io/ioutil"
	"log"
	"net/http"
	"os"
	"path"
	"path/filepath"
	"strings"
	"time"
)

func checkErrFatal(err error) {
	if err != nil {
		log.Fatalln(err)
	}
}

func downloadFile(query, filepath string) int {
	var code int

	// Get the data
	client := http.Client{Timeout: 60 * time.Second}
	req, err := http.NewRequest("GET", query, nil)
	checkErrFatal(err)
	req.Header.Add("User-Agent", "Mozilla/5.0 (Nice crawler for extracting German birds and sounds. See github.com/gojibjib - Thank you)")

	resp, err := client.Do(req)
	if err != nil {
		log.Println(err)
		return 500
	}
	defer resp.Body.Close()

	// Assigning to prevent timeout
	content := resp.Body

	// Check status code
	code = resp.StatusCode
	if code != http.StatusOK {
		log.Printf("Bad status: %d", resp.StatusCode)
		return code
	}

	// Creating the file
	out, err := os.Create(filepath)
	checkErrFatal(err)
	defer out.Close()

	// Write to file
	_, err = io.Copy(out, content)
	if err != nil {
		log.Println(err)
		return 500
	}
	return code
}

func main() {
	// Load JSON
	var dlMap map[string][]string
	jsonName := "dl_dict.json"
	filesDir, _ := filepath.Abs("../files")

	jsonFile, err := ioutil.ReadFile(jsonName)
	checkErrFatal(err)

	err = json.Unmarshal(jsonFile, &dlMap)
	checkErrFatal(err)

	// URL things
	url := "https://www.xeno-canto.org"
	n := len(dlMap)
	var c int

	for k, v := range dlMap {
		name := strings.Replace(k, "-", "_", -1)

		fmt.Printf("%d/%d - %s\n", c+1, n, name)

		maxDl := len(v)
		for idx, id := range v {
			idFile := strings.Replace(id, "/", "", -1)
			fName := fmt.Sprintf("%s-%s.mp3", name, idFile)
			fPath := path.Join(filesDir, name, fName)

			// Download, if file is missing
			if _, err := os.Stat(fPath); os.IsNotExist(err) {
				fmt.Printf("%d/%d: %s ", idx+1, maxDl, id)
				currUrl := fmt.Sprintf("%s%s/download", url, id)
				downloadFile(currUrl, fPath)
				time.Sleep(500 * time.Millisecond)
			}
		}
		fmt.Println()
		c++
	}
}
