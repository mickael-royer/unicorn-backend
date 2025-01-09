package app

import (
	"context"
	"fmt"
	"log"
)

// GetFileFromDapr retrieves file content from Dapr state store
func (a *App) GetFileFromDapr(key string) (string, error) {
	ctx := context.Background()                                   // Create a context
	state, err := a.daprClient.GetState(ctx, DaprStateStore, key) // Remove the nil
	if err != nil {
		return "", fmt.Errorf("failed to get state from Dapr: %w", err)
	}

	if state == nil || len(state.Value) == 0 {
		return "", fmt.Errorf("file with ID '%s' not found", key)
	}

	fileData := string(state.Value)
	log.Printf("File content retrieved from dapr: %s", fileData)

	return fileData, nil
}
