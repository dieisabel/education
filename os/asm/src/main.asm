; Simple FASM program that just reads symbol from user input and writes it to file
; Created with help from https://stackoverflow.com/questions/8312290/how-to-open-a-file-in-assembler-and-modify-it,
; FASM manual and unistd_32.h that contains system calls (idk where located this file in your system, maybe in
; /usr/include/asm/unistd_32.h)

format ELF64 executable
entry main

; TODO: add segments (or sections idk)
input    rb 1
buffer   rq 1 ; Buffer for file descriptor
filename db "out/data.txt", 0

main:
    call readUserInput
    call writeToFile
    call exit

readUserInput:
    mov rax, 3     ; 3 - read system call
    mov rbx, 0     ; 0 - stdin
    mov rcx, input ; Buffer address
    mov rdx, 1     ; Amount of bytes to read
    int 0x80       ; Initiate interrupt

writeToFile:
    call openOrCreateFile
    call writeSymbol
    call closeFile

    openOrCreateFile:
        mov rax, 5        ; 5 - open
        mov rbx, filename ; Set filename
        mov rcx, 0102o    ; Read and write mode, also if file doesn't exists
                          ; create it
        mov rdx, 0666o    ; Set permissions for new file if created
        int 0x80          ; Initiate interrupt
        mov [buffer], rax ; Copy file descriptor in buffer

    writeSymbol:
        mov rax, 4        ; 4 - write
        mov rbx, [buffer] ; Set file descriptor
        mov rcx, input    ; Set user input
        mov rdx, 1        ; Set 1 byte of input
        int 0x80          ; Initiate interrupt

    closeFile:
        mov rax, 6        ; 6 - close
        mov rbx, [buffer] ; Set file descriptor
        int 0x80          ; Initiate interrupt

exit:
    mov rax, 1 ; 1 - exit system call
    mov rbx, 0 ; 0 - status code
    int 0x80   ; Initiate interrupt
