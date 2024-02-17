# FroYo
Repo contains the interpreter and example programs for the FROYO programming language. 

FroYo is a double-half-deque-and-stack language that is modeled after a classic frozen yogurt machine with vanilla, chocolate, and vanilla/chocolate swirl. Data is put into each flavor deque and is then scooped or poured out to the serving cone stack. 

Instructions are separated by a new line. 
Lines beginning with "#" are treated as comments. 

## Grammar
```
<program> → CLOCKIN \n <expr_list> \n CLOCKOUT
<expr_list> →
    <expr> 
    <expr>\n<expr_list>
<expr> → 
    <instr>
    <instr> X <expr>
    <instr> ? <expr>
<instr> → 
    <literal>
    POUR <flavor>
    SPILL <flavor>
    SCOOP (<flavor> | <literal>)
    HOWMUCH <container>
    REFILL <flavor> <expr>
    STIR <flavor>
    SWIRL [<operator>]
    LRIWS [<operator>]
    ORDER <flavor>
    SERVE
    OOPS <flavor>
    HOLD <expr>
<literal> → 
    [0-9]
    “<alphanumeric_string>”
<container> → 
    CONE
    <flavor>
<flavor> →
    VANILLA
    CHOCOLATE
```

## Detailed Description
Containers `<container>`:
- Flavors `<flavor>`:
  - VANILLA
  - CHOCOLATE
- CONE

Instruction Set `<instr>`: 

| CLOCKIN | Start program |
| CLOCKOUT | End program |

Input/Output from Flavor Deques
- SCOOP (`<flavor>` | `<literal>`)
  - Take the specified value or the next item from the end of the specified flavor deque and put it onto the serving cone stack. 
- POUR `<flavor>`
  - Take the next item from the beginning of the specified flavor deque and put it onto the serving cone stack. 
- SPILL `<flavor>`
  - Take the next item from the beginning of the specified flavor deque and discard it. 
- REFILL`<flavor>` `<expr>`
  - Put the output of the expression at the end of the specified flavor deque. 
- OOPS `<flavor>`
  - Takes a value from the top of the serving cone stack and puts it at the end of the specified flavor deque. 
- SWIRL [`<operator>`]
  - Take the next item from the beginning of both deques and apply the specified operator in the order: <vanilla> <op> <chocolate>. The output is put onto the serving cone stack. 
  - If no operator is specified, perform addition. 
- LRIWS [<operator>]
  - Take the next item from the beginning of both deques and apply the specified operator in the order: <chocolate> <op> <vanilla>. The output is put onto the serving cone stack. 
If no operator is specified, perform addition. 
Check/Modify Flavor Deques
HOWMUCH <cont>
Outputs the number of items in the specified container to the serving cone. 
If the specified container is the cone, the number of items before executing the command are put onto the cone
E.g. If the cone has the contents [‘a’, ‘b’, ‘c’], the number 3 will be added to the cone: [‘a’, ‘b’, ‘c’, 3]
STIR <flavor>
Reverse the order of items in the specified flavor deque. 
Console Input/Output
ORDER <flavor>
Take input from the console and put it on the specified flavor deque. 
The input is put at the end of the flavor deque, with the beginning of the input closest to the beginning of the deque. 
If the input is alphanumeric, it is read in character-by-character as a string. 
If the input is numeric, it is read in as a single number. 
SERVE
Output the contents of the serving cone stack to the console and clear the serving cone stack. 
Contents are output from top to bottom. 
Looping and Conditionals
HOLD <instr>
Performs the given instruction, but does not remove values from flavor deques or the serving cone stack. 
<instr> X <expr>
Repeats the specified expression a number of times specified by the instruction. 
If <instr> evaluates to a decimal number, the decimal portion is truncated. 
If <instr> evaluates to a value <= 0, the instruction is not executed 
<instr> ? <expr>
Only executes the following instruction if the given expression is: 
A number greater than 0
A non-empty string 

The <expr> Value: 
An <expr> can be: 
A string literal 
An integer literal
Any command that outputs to the serving cone. Instead of outputting to the serving cone, though, it will be consumed and used in the expression. 
The HOLD keyword can be used before an expression command to prevent the value from being consumed, if the command takes a value from a container 
<expr> can only contain commands or literals. They cannot contain arithmetic operations. 
To perform arithmetic, use the SWIRL command

