package main

import (
	_ "database/sql"
	"fmt"
	"github.com/gin-gonic/gin"
	"github.com/joho/godotenv"
	"net/http"
	"os"
	"os/signal"
	"path/filepath"
	"server/database"
	// "github.com/gin-contrib/cors"
	_ "github.com/lib/pq"
)

func initRouter() *gin.Engine {
	gin.SetMode(gin.ReleaseMode)

	engine := gin.Default()

	// Routes
	engine.GET("/", func(context *gin.Context) {
		context.String(200, "Under Construction...")
	})

	// ...

	return engine
}

func main() {
	x, err := os.Executable()
	if err != nil {
		panic(err)
	}

	if err := godotenv.Load(fmt.Sprintf("%s\\.env", filepath.Dir(x))); err != nil {
		panic(err)
	}

	var (
		host     = os.Getenv("PG_HOST")
		port     = 5432 // Hardcoded for now, will fix later
		username = os.Getenv("PG_USER")
		password = os.Getenv("PG_PASSWORD")
		dbname   = os.Getenv("PG_DB")
	)

	login := fmt.Sprintf("host=%s port=%d user=%s password=%s dbname=%s sslmode=disable",
		host, port, username, password, dbname)

	db, err := database.Connect(login)
	if err != nil {
		panic(err)
	}

	router := initRouter()

	server := &http.Server{
		Addr:    ":8080",
		Handler: router,
	}

	stop := make(chan os.Signal)
	signal.Notify(stop, os.Interrupt)

	go func() {
		<-stop
		if err := server.Close(); err != nil {
			fmt.Println(err.Error())
		}

		if err := db.Close(); err != nil {
			fmt.Println(err.Error())
		}
	}()

	if err = server.ListenAndServe(); err != nil {
		fmt.Println(err.Error())
	}
}
