package main

import (
	"fmt"
	"os"
	"syscall"
)

func main() {
	// TODO: add processing logic
	fmt.Println("THIS SHOULD PRINT WHEN THERE IS AT LEAST 1 MESSAGE IN THE SQS QUEUE!")
	for true {
		continue
	}
	os.Exit(int(syscall.SIGTERM))
}
