package main

import (
	"log"

	"github.com/hajimehoshi/ebiten/v2"
	"github.com/hajimehoshi/ebiten/v2/ebitenutil"
)

type Game struct{}

func (g *Game) Update() error {
	// Update game logic here
	return nil
}

func (g *Game) Draw(screen *ebiten.Image) {
	// Draw game elements here
	ebitenutil.DebugPrint(screen, "Hello, Ebiten!")
}

func (g *Game) Layout(outsideWidth, outsideHeight int) (int, int) {
	// Return the size of the game window
	return 640, 480
}

func main() {
	ebiten.SetWindowSize(640, 480)
	ebiten.SetWindowTitle("Hello Ebiten")

	game := &Game{}
	if err := ebiten.RunGame(game); err != nil {
		log.Fatal(err)
	}
}

// This code initializes a simple Ebiten game that displays "Hello, Ebiten!" on the screen.
// It sets the window size and title, implements the game loop with update, draw, and
