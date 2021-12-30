package database

import (
	"database/sql"
	_ "github.com/lib/pq"
)

func Connect(login string) (*sql.DB, error) {
	connection, err := sql.Open("postgres", login)
	if err != nil {
		return nil, err
	}

	if err = connection.Ping(); err != nil {
		return nil, err
	}

	return connection, nil
}
