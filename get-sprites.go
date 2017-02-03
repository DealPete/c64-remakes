package main

import "bytes"
import "fmt"
import "image"
import "image/color"
import "image/png"
import "io/ioutil"
import "os"

var (
	COLOR_NONE = color.RGBA{0, 0, 0, 0}
	COLOR_BLACK = color.RGBA{0,0,0,255}
	COLOR_WHITE = color.RGBA{255,255,255,255}
	COLOR_RED = color.RGBA{136,0,0,255}
	COLOR_CYAN = color.RGBA{170,255,238,255}
	COLOR_VIOLET = color.RGBA{204,68,204,255}
	COLOR_GREEN = color.RGBA{0,204,85,255}
	COLOR_BLUE = color.RGBA{0,0,170,255}
	COLOR_YELLOW = color.RGBA{238,238,119,255}
	COLOR_ORANGE = color.RGBA{221,136,85,255}
	COLOR_BROWN = color.RGBA{102,68,0,255}
	COLOR_LIGHTRED = color.RGBA{255,119,199,255}
	COLOR_GREY1 = color.RGBA{51,51,51,255}
	COLOR_GREY2 = color.RGBA{119,119,119,255}
	COLOR_LIGHTGREEN = color.RGBA{170,255,102,255}
	COLOR_LIGHTBLUE = color.RGBA{0,136,255,255}
	COLOR_GREY3 = color.RGBA{187,187,187,255}
)

var colors = []color.RGBA{COLOR_BLACK, COLOR_WHITE, COLOR_RED, COLOR_CYAN,
	COLOR_VIOLET, COLOR_GREEN, COLOR_BLUE, COLOR_YELLOW, COLOR_ORANGE,
	COLOR_BROWN, COLOR_LIGHTRED, COLOR_GREY1, COLOR_GREY2, COLOR_LIGHTGREEN,
	COLOR_LIGHTBLUE, COLOR_GREY3}

func output_monochrome_sprite(sprite []byte, filename string,
	color color.RGBA) {
    img := image.NewRGBA(image.Rect(0, 0, 24, 21))

	for i := 0; i < 63; i++ {
		var mask uint8
		mask = 128
		for bit := 0; bit < 8; bit++ {

			set_color := COLOR_NONE
			if (uint8(sprite[i]) & mask != 0) {
				set_color = color
			}
			img.Set((i % 3) * 8 + bit, i / 3, set_color)
			mask >>= 1
		}
	}

    imgFile, _ := os.OpenFile(filename, os.O_WRONLY|os.O_CREATE, 0600)
    defer imgFile.Close()
    png.Encode(imgFile, img)
}

func output_multicolor_sprite(sprite []byte, filename string,
	color01 color.RGBA, color10 color.RGBA, color11 color.RGBA) {
    img := image.NewRGBA(image.Rect(0, 0, 24, 21))

	for i := 0; i < 63; i++ {
		for bit := 0; bit < 4; bit++ {
			bits := uint8(sprite[i]) >> (uint8(3 - bit) * 2) & 3
			set_color := COLOR_NONE
			if bits == 1 {
				fmt.Print("==")
				set_color = color01
			} else if bits == 2 {
				fmt.Print("//")
				set_color = color10
			} else if bits == 3 {
				fmt.Print("~~")
				set_color = color11
			} else {
				fmt.Print("00")
			}
			img.Set((i % 3) * 8 + (bit * 2), i / 3, set_color)
			img.Set((i % 3) * 8 + (bit * 2) + 1, i / 3, set_color)
		}
		if i % 3 == 2 {
			fmt.Print("\n")
		}
	}

    imgFile, _ := os.OpenFile(filename, os.O_WRONLY|os.O_CREATE, 0600)
    defer imgFile.Close()
    png.Encode(imgFile, img)
}

func main() {
	imageFile := os.Args[1];
	f, err := os.Open(imageFile)
	if err != nil {
		panic(err)
	}
	defer f.Close()

	fileData, _ := ioutil.ReadAll(f)

	ram_magic := []byte{0x43, 0x36, 0x34, 0x4D, 0x45, 0x4D}
	vic_magic := []byte{0x56, 0x49, 0x43, 0x2d, 0x49, 0x49}
	ram_start := bytes.Index(fileData, ram_magic) + 0x1a
	vic_start := bytes.Index(fileData, vic_magic) + 0x475
	ram := fileData[ram_start:ram_start + 0x10000]
	vic := fileData[vic_start:vic_start + 0x2f]
	sprite_count := 0

	for i := 0; i < 8; i++ {
		if vic[0x15] & (1 << uint8(i)) != 0 {
			sprite_pointer := ram[0x7f8 + i]
			sprite_start := 64 * int(sprite_pointer)
			sprite := ram[sprite_start:sprite_start + 63]
			if vic[0x1c] & (1 << uint8(i)) == 0 {
				output_monochrome_sprite(sprite,
					"sprite" + string(sprite_count + 0x30) + ".png",
					colors[vic[0x27 + i]])
			} else {
				output_multicolor_sprite(sprite,
					"sprite" + string(sprite_count + 0x30) + ".png",
					colors[vic[0x25]], colors[vic[0x27 + i]],
					colors[vic[0x26]])
			}
			sprite_count += 1
		}
	}

	fmt.Print("Found ", sprite_count, " sprite(s).")
}
