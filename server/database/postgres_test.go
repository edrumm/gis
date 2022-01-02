package database

import (
	"fmt"
	"github.com/joho/godotenv"
	"os"
	"testing"
)

func TestConnect(t *testing.T) {
	// Use /bin path for reference
	if err := godotenv.Load("../.env"); err != nil {
		t.Fatalf("Error %s\n", err.Error())
	}

	var (
		host     = os.Getenv("PG_HOST")
		port     = 5432
		username = os.Getenv("PG_USER")
		password = os.Getenv("PG_PASSWORD")
		dbname   = os.Getenv("PG_DB")
	)

	db, err := Connect(fmt.Sprintf("host=%s port=%d user=%s password=%s dbname=%s sslmode=disable",
		host, port, username, password, dbname))

	if err != nil {
		t.Fatalf("Error %s\n", err.Error())
	}

	_ = db.Close()
}

// Add more tests
