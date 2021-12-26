package database

import (
	"database/sql"
	"fmt"

	_ "github.com/lib/pq"
)

func Connect() (*sql.DB, error) {
	login := fmt.Sprintf("") // need credentials for DB

	connection, err := sql.Open("postgres", login)
	if err != nil {
		return nil, err
	}

	err = connection.Ping()
	if err != nil {
		return nil, err
	}

	return connection, nil
}
