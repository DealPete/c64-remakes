package main

import "fmt"
import "image"
import "image/color"
import "image/png"
import "io/ioutil"
import "os"

func main() {
	imageFile := os.Args[1];
	f, err := os.Open(imageFile)
	if err != nil {
		panic(err)
	}
	defer f.Close()

	bytes, _ := ioutil.ReadAll(f)

	fmt.Print("%s", bytes)
/*
    // Create an 100 x 50 image
    img := image.NewRGBA(image.Rect(0, 0, 100, 50))

    // Draw a red dot at (2, 3)
    img.Set(2, 3, color.RGBA{255, 0, 0, 255})

    // Save to out.png
    f, _ := os.OpenFile("out.png", os.O_WRONLY|os.O_CREATE, 0600)
    defer f.Close()
    png.Encode(f, img)*/
}
