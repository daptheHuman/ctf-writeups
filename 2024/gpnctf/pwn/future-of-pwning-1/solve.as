const section read ip                          
// text strings
filename:   int8 "/flag", 0                    
mode: int8 "r", 0                              
const end

bss section datap uninitialized                  
int64 buf[0x100]                                 
bss end

code section execute                             
extern _fopen: function                          
extern _fgets: function                          
extern _puts: function                           
extern _fclose: function                         
extern _exit: function                           

_main function public                            

// Open the file
int64 r0 = address([filename])                   
int64 r1 = address([mode])                       
call _fopen                                      
int64 r2 = r0                                    

// Read from the file
int64 r0 = address([buf])                        
int64 r1 = 256                                   
int64 r3 = r2                                    
call _fgets                                      

// Print the buffer
int64 r0 = address([buf])                        
call _puts                                       

// Close the file
int64 r0 = r2                                   
call _fclose                                    

// Exit the program successfully
int64 r0 = 0                                     
call _exit                                       

_main end

code end
