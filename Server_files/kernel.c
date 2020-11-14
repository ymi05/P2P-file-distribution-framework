#define VGA_ADDRESS 0xB8000	/* video memory begins here. */

/* Some font colors you can use */
#define BLACK 0
#define GREEN 2
#define RED 4
#define YELLOW 14
#define WHITE_COLOR 15

#define KEYBOARD_PORT 0x60

#define KEY_A 0x1E
#define KEY_B 0x30
#define KEY_C 0x2E
#define KEY_D 0x20
#define KEY_E 0x12
#define KEY_F 0x21
#define KEY_G 0x22
#define KEY_H 0x23
#define KEY_I 0x17
#define KEY_J 0x24
#define KEY_K 0x25
#define KEY_L 0x26
#define KEY_M 0x32
#define KEY_N 0x31
#define KEY_O 0x18
#define KEY_P 0x19
#define KEY_Q 0x10
#define KEY_R 0x13
#define KEY_S 0x1F
#define KEY_T 0x14
#define KEY_U 0x16
#define KEY_V 0x2F
#define KEY_W 0x11
#define KEY_X 0x2D
#define KEY_Y 0x15
#define KEY_Z 0x2C
#define KEY_SPACE 0x39
#define KEY_ENTER 0x1C

#define MAX_LINE_LENGTH 10

unsigned short *terminal_buffer;
unsigned int vga_index;
unsigned int next_line_index = 1;
unsigned int lines_count = 0;

char* command[MAX_LINE_LENGTH];
unsigned int command_length = 0;
char whatami[7] = "whatami";




void clear_screen(void)
{
	int index = 0;
	/* there are 25 lines each of 80 columns;
	   each element takes 2 bytes */
	while (index < 80 * 25 * 2) {
		terminal_buffer[index] = ' ';
		index += 1;
	}
	next_line_index = 1;
}

void print_new_line()
{
	if(next_line_index >= 24){
		next_line_index = 0;
		clear_screen();
	}
	vga_index = 80*next_line_index;
	next_line_index++;
}

void print_string(char *str, unsigned char color)
{
	int index = 0;
	while (str[index]) {
		terminal_buffer[vga_index] = (unsigned
		 short)str[index]|(unsigned short)color << 8;
		index++;
		vga_index++;
	}
	print_new_line();
}
void print_char(char c, unsigned char color)
{
	terminal_buffer[vga_index] = (unsigned
		  short)c|(unsigned short)color << 8;
	vga_index++;
}



char get_ascii_char(char keycode)
{
	if(keycode == KEY_A){
		return 'a';
	}
	else if(keycode == KEY_B){
		return 'b';
	}
	else if(keycode == KEY_C){
		return 'c';
	}
	else if(keycode == KEY_D){
		return 'd';
	}
	else if(keycode == KEY_E){
		return 'e';
	}
	else if(keycode == KEY_F){
		return 'f';
	}
	else if(keycode == KEY_G){
		return 'g';
	}
	else if(keycode == KEY_H){
		return 'h';
	}
	else if(keycode == KEY_I){
		return 'i';
	}
	else if(keycode == KEY_J){
		return 'j';
	}
	else if(keycode == KEY_K){
		return 'k';
	}
	else if(keycode == KEY_L){
		return 'l';
	}
	else if(keycode == KEY_M){
		return 'm';
	}
	else if(keycode == KEY_N){
		return 'n';
	}
	else if(keycode == KEY_O){
		return 'o';
	}
	else if(keycode == KEY_P){
		return 'p';
	}
	else if(keycode == KEY_Q){
		return 'q';
	}
	else if(keycode == KEY_R){
		return 'r';
	}
	else if(keycode == KEY_S){
		return 's';
	}
	else if(keycode == KEY_T){
		return 't';
	}
	else if(keycode == KEY_U){
		return 'u';
	}
	else if(keycode == KEY_V){
		return 'v';
	}
	else if(keycode == KEY_W){
		return 'w';
	}
	else if(keycode == KEY_X){
		return 'x';
	}
	else if(keycode == KEY_Y){
		return 'y';
	}
	else if(keycode == KEY_Z){
		return 'z';
	}
	else if(keycode == KEY_SPACE){
		return -1;
	}
	else{
		return ' ';
	}
}

// keyboard

unsigned char inb(unsigned short port)
{
	unsigned char ret;
	asm volatile("inb %1, %0" : "=a"(ret) : "d"(port));
	return ret;
}

void outb(unsigned short port, unsigned char data)
{
	asm volatile("outb %0, %1" : "=a"(data) : "d"(port));
}

char get_input_keycode()
{
	char ch = 0;
	while((ch = inb(KEYBOARD_PORT)) != 0){
	  if(ch > 0)
	    return ch;
	}
	return ch;
}

/*
keep the cpu busy for doing nothing(nop)
*/
void wait_for_io(unsigned int timer_count)
{
	while(1){
	asm volatile("nop");
	timer_count--;
	if(timer_count <= 0)
	  break;
	}
}

void sleep(unsigned int timer_count)
{
	wait_for_io(timer_count);
}
// command

void reset_command(){


	command_length = 0;
	for(int i=0;i<MAX_LINE_LENGTH;i++){
		command[i] = '\0';
	}
	
}

void check_command(void)
{
	if(command_length == 7)
	{
		for(int i=0;i<command_length+1;i++){
		
			if(command[i] != whatami[i]){
			
				print_string("Unfamiliar command, try whatami.", WHITE_COLOR);
				return;
			}
		}
		print_string("I am the CMPS 272 shell", WHITE_COLOR);
	}
	else
	{
		print_string("Unfamiliar command, try whatami.", WHITE_COLOR);
	}
}

void add_to_command(char ch){

	command[command_length] = ch;
	command_length++;
	
	
}
void test_input()
{
	char ch = 0;
	char keycode = 0;
	do{
		keycode = get_input_keycode();
		if(keycode == KEY_ENTER){
			print_new_line();
			check_command();
			reset_command();
		}else{
			if(command_length < MAX_LINE_LENGTH){
				ch = get_ascii_char(keycode);
				print_char(ch, WHITE_COLOR);
				add_to_command(ch);
			}
			
			
		}
		sleep(0x04FFFFFF);
	}while(ch >= 0);
}
void main(void)
{
	reset_command();
	terminal_buffer = (unsigned short *)VGA_ADDRESS;
	vga_index = 0;
	
	clear_screen();
	
	print_string("Hello from CMPS 272!", WHITE_COLOR);
	
	test_input();
	
	print_new_line();
	
	print_string("Goodbye from CMPS 272!", WHITE_COLOR);
	return;
}

