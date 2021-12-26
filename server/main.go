package main

import (
	_ "database/sql"
	"fmt"
	"github.com/gin-gonic/gin"
	"server/database"

	// "github.com/gin-contrib/cors"
	_ "github.com/lib/pq"
)

func newEngine() *gin.Engine {
	engine := gin.Default()

	// Routes
	engine.GET("/", func(context *gin.Context) {
		context.String(200, "Under Construction...")
	})

	// ...

	return engine
}

func main() {
	db, err := database.Connect()
	if err != nil {
		panic(err)
	}

	fmt.Println("Connected!")

	defer func() {
		if err := db.Close(); err != nil {
			panic(err)
		}
	}()

	engine := newEngine()
	engine.Run(":8080")
}
