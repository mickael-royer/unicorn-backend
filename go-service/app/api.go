package app

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"

	"github.com/dapr/go-sdk/client"
	"github.com/gorilla/mux"
	"github.com/joho/godotenv"
)

type App struct {
	Router     *mux.Router
	daprClient client.Client
}

func (a *App) Initialize(daprClient client.Client) {
	a.daprClient = daprClient

	// Load .env file
	err := godotenv.Load()
	if err != nil {
		log.Printf("Error loading .env file: %v", err)
	}

	a.Router = mux.NewRouter()
	a.Router.HandleFunc("/github/push-file", a.PushFileToGitHubHandler).Methods("POST")
}

// PushFileToGitHubHandler handles pushing a new file to a GitHub repository
func (a *App) PushFileToGitHubHandler(w http.ResponseWriter, r *http.Request) {
	log.Println("Entering PushFileToGitHubHandler method")

	type RequestPayload struct {
		FileId  string `json:"fileId"` //add fileId to retrieve file content
		Message string `json:"message"`
	}
	// Decode the request payload
	log.Println("Decoding the request payload")
	var payload RequestPayload
	err := json.NewDecoder(r.Body).Decode(&payload)
	if err != nil {
		log.Printf("Error during decoding request payload : %v", err)
		http.Error(w, "Invalid request payload", http.StatusBadRequest)
		return
	}
	log.Printf("Request payload decoded: %+v\n", payload)
	// Retrieve file content from Dapr state store
	fileData, err := a.GetFileFromDapr(payload.FileId)
	if err != nil {
		log.Printf("Error getting file from dapr: %v", err)
		http.Error(w, fmt.Sprintf("Failed to retrieve file from Dapr: %v", err), http.StatusInternalServerError)
		return
	}
	log.Printf("File content retrieved: %s", fileData)

	a.PushFileToGitHub(payload.FileId, fileData, payload.Message, w)
}

func (a *App) Run(addr string) {
	log.Fatal(http.ListenAndServe(addr, a.Router))
}
