package app

import "os"

// GitHub configuration
var (
	RepoOwner       = "mickael-royer"        // set to your repository owner
	RepoName        = "unicorn-hugo-website" // set to your repository name
	TargetDirectory = "content/posts"        // set to the desired target directory
)

// Dapr Configuration
const (
	DaprStateStore = "filestore"
)

// Get GITHUB_TOKEN from the .env file
func GetGitHubToken() string {
	return os.Getenv("GITHUB_TOKEN")
}
