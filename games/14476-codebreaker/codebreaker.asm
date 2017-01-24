    BITS 16
    
    mov ax, 0800h	; put the stack pointer at the 
    cli				; end of the 64k segment.
    mov ss, ax
    mov sp, 0xFFFF
    sti				; disable interrupts while changing stack

    mov ax, 07C0h	; set data segment to beginning of program in memory
    mov ds, ax

	mov ah, 00h
	mov al, 0dh
	int 10h			; switch to 40x25 mode.

	mov ah, 0bh
	mov bx, 08h 
	int 10h			; change background color to dark grey.

; ---------------------------------------------------------------------
; print titleMessage

	mov bl, 0fh
	mov cx, 01h
	mov dh, 16h
	mov dl, 08h

    mov si, titleMessage

repeat:
	mov ah, 02h
	int 10h			; move cursor
	inc dl

    lodsb
    cmp al, 0
    je done		

    mov ah, 09h
    int 10h	
    jmp repeat
done:

; ---------------------------------------------------------------------
; print starting code

	mov bl, 00h
	mov cx, 1
	mov dh, 17h
	mov dl, 0ch
	mov ah, 02h
	int 10h
	mov ah, 0Eh
	mov al, 09h
	int 10h

	mov al, 07h
	mov cx, 3
	mov dl, 0dh
	mov ah, 02h
	int 10h
	mov ah, 09h
	int 10h
   
; ---------------------------------------------------------------------
; To use int 13h, we must convert the logical address to CHS form - see
; https://en.wikipedia.org/wiki/Logical_block_addressing#CHS_conversion

    mov cl, 2		; the program is in sector 1
    mov dh, 0		; on head 0
	mov ch, 0		; on track 0

    mov ax, 0x800
	mov ds, ax
    mov es, ax

    mov ah, 2		; read program from disk
    mov al, 64		; assume program is 64K
    mov dl, 80h
    mov bx, 0h

    int 13h

   	jmp 0x800:0000

; ---------------------------------------------------------------------
; VARIABLES
    titleMessage db "::: x86 CODEBREAKER :::", 0
    
    times 510-($-$$) db 0

    dw 0xAA55		; The standard PC boot signature
