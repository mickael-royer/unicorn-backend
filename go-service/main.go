package main

import (
	"fmt"
	"log"
	"os"

	"github.com/mickael-royer/unicorn-dapr/go-service/app"

	dapr "github.com/dapr/go-sdk/client"
)

func main() {
	a := app.App{}

	client, err := dapr.NewClient()
	if err != nil {
		log.Fatalf("Error creating Dapr client: %v", err)
	}
	defer client.Close()

	a.Initialize(client)

	port, ok := os.LookupEnv("PORT")
	if !ok {
		port = "8050"
	}

	binding := fmt.Sprintf(":%s", port)

	a.Run(binding)
}
