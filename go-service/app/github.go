package app

import (
	"bytes"
	"encoding/base64"
	"encoding/json"
	"fmt"
	"io"
	"log"
	"net/http"
	"strings"
)

// PushFileToGitHub handles pushing a new file to a GitHub repository
func (a *App) PushFileToGitHub(fileId string, fileData string, message string, w http.ResponseWriter) {

	fileName := fmt.Sprintf("%s.md", fileId)

	// GitHub API configuration
	gitHubAPIURL := fmt.Sprintf("https://api.github.com/repos/%s/%s/contents/%s/%s", RepoOwner, RepoName, TargetDirectory, fileName)
	log.Printf("Github API URL: %s", gitHubAPIURL)
	token := GetGitHubToken() // Ensure your GitHub token is set as an environment variable
	log.Println("Github token retrieved.")

	// unmarshall the json content:
	var fileDataMap map[string]interface{}
	err := json.Unmarshal([]byte(fileData), &fileDataMap)
	if err != nil {
		log.Printf("Error unmarshalling file data: %v", err)
		http.Error(w, "Failed to unmarshal file data", http.StatusInternalServerError)
		return
	}
	// Ensure "content" key exists and is a string
	content, ok := fileDataMap["content"].(string)
	if !ok {
		log.Println("Error extracting content from data")
		http.Error(w, "Content not found or invalid", http.StatusInternalServerError)
		return
	}

	// Ensure "synthesis" key exists and is a string
	synthesis, ok := fileDataMap["synthesis"].(string)
	if !ok {
		log.Println("Error extracting synthesis from data")
		http.Error(w, "Synthesis not found or invalid", http.StatusInternalServerError)
		return
	}

	// Replace \n with actual newline characters
	content = strings.ReplaceAll(content, "\\n", "\n")
	synthesis = strings.ReplaceAll(synthesis, "\\n", "\n")

	// combine content and synthesis into markdown format
	markdownContent := fmt.Sprintf("%s\n\n# Analysis\n%s", content, synthesis)
	log.Printf("markdown content created: %s", markdownContent)

	// Prepare the file content (Base64 encode required by GitHub API)
	contentEncoded := base64.StdEncoding.EncodeToString([]byte(markdownContent))

	// Check if the file exists to fetch the sha, so we can correctly update it
	req, err := http.NewRequest("GET", gitHubAPIURL, nil)
	if err != nil {
		log.Printf("Error creating github GET request: %v", err)
		http.Error(w, "Failed to create GitHub API request", http.StatusInternalServerError)
		return
	}
	req.Header.Set("Authorization", "Bearer "+token)
	req.Header.Set("Accept", "application/vnd.github.v3+json")
	client := &http.Client{}
	resp, err := client.Do(req)
	var body []byte // Declare body variable here
	var requestBody map[string]string

	if err == nil && resp.StatusCode == http.StatusOK {
		defer resp.Body.Close()
		body, err = io.ReadAll(resp.Body)
		if err != nil {
			log.Printf("Error reading response from github api: %v", err)
			http.Error(w, "Failed to read response from GitHub API", http.StatusInternalServerError)
			return
		}
		type githubResponse struct {
			Sha string `json:"sha"`
		}
		var gitHubResponse githubResponse
		if err := json.Unmarshal(body, &gitHubResponse); err != nil {
			log.Printf("Error unmarshalling github response: %v", err)
			http.Error(w, "Failed to unmarshal response from GitHub API", http.StatusInternalServerError)
			return
		}

		log.Printf("File already exists, retrieving SHA: %s", gitHubResponse.Sha)

		// Build the request body
		log.Println("Building the request body")
		requestBody = map[string]string{
			"message": message,
			"content": contentEncoded,
			"sha":     gitHubResponse.Sha,
		}
	} else {
		// Build the request body
		log.Println("Building the request body")
		requestBody = map[string]string{
			"message": message,
			"content": contentEncoded,
		}
	}

	requestBodyJSON, err := json.Marshal(requestBody)
	if err != nil {
		log.Printf("Error during encode request body : %v", err)
		http.Error(w, "Failed to encode request body", http.StatusInternalServerError)
		return
	}
	log.Printf("Request body build: %s", string(requestBodyJSON))

	// Send the request to GitHub API
	req, err = http.NewRequest("PUT", gitHubAPIURL, bytes.NewBuffer(requestBodyJSON))
	if err != nil {
		log.Printf("Error creating request to Github api: %v", err)
		http.Error(w, "Failed to create GitHub API request", http.StatusInternalServerError)
		return
	}
	log.Println("Request to github API created.")

	req.Header.Set("Authorization", "Bearer "+token)
	req.Header.Set("Accept", "application/vnd.github.v3+json")

	resp, err = client.Do(req)
	if err != nil {
		log.Printf("Error during http call to github api : %v", err)
		http.Error(w, "Failed to send request to GitHub API", http.StatusInternalServerError)
		return
	}
	defer resp.Body.Close()
	log.Println("Request to github API done.")

	// Read and respond with GitHub's response
	log.Println("Reading response from github API")
	body, err = io.ReadAll(resp.Body)
	if err != nil {
		log.Printf("Error during read response body from github api : %v", err)
		http.Error(w, "Failed to read response from GitHub API", http.StatusInternalServerError)
		return
	}
	log.Printf("Response from github API received: %s", string(body))

	if resp.StatusCode != http.StatusCreated && resp.StatusCode != http.StatusOK {
		log.Printf("Github API returned an error : %s", string(body))
		http.Error(w, fmt.Sprintf("GitHub API error: %s", string(body)), resp.StatusCode)
		return
	}
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(resp.StatusCode)
	w.Write(body)
	log.Println("Response sent to the python microservice.")
}
