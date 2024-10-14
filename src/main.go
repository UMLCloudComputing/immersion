package main

import (
	"fmt"
	"os"
	"os/signal"
	"syscall"

	"github.com/bwmarrin/discordgo"
	"github.com/joho/godotenv"
)

func messageCreate(session *discordgo.Session, message *discordgo.MessageCreate) {
	// only do something on message if not created by bot
	if message.Author.ID != session.State.User.ID {
		switch message.Content {
		case "$ping":
			session.ChannelMessageSend(message.ChannelID, "Pong!")
		case "$pong":
			session.ChannelMessageSend(message.ChannelID, "Ping!")
		}
	}
}

func main() {

	godotenv.Load("../.env")

	discord, err := discordgo.New("Bot " + os.Getenv("DISCORD_TOKEN"))
	if err != nil {
		fmt.Println("Error creating Discord session, ", err)
		os.Exit(1)
	}

	discord.AddHandler(messageCreate)
	discord.Identify.Intents = discordgo.IntentsGuildMessages

	err = discord.Open()
	if err != nil {
		fmt.Println("Error opening connection, ", err)
		os.Exit(1)
	}

	fmt.Println("Bot is now running, hit CTRL+C to exit!")
	sc := make(chan os.Signal, 1)
	signal.Notify(sc, syscall.SIGINT, syscall.SIGTERM, os.Interrupt)
	<-sc

	discord.Close()
}
