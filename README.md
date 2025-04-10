# ✧･ﾟ: *✧･ﾟ Nyx CLI Libwawy ･ﾟ✧*:･ﾟ✧

**Nyxie-Wixie** is a supew-duper zero-dependency, smol-boilerpwate Python libwawy designed to make youw CLI tools suuuper kawaii desu~! It gives you coworfuw and customizable output, custom awgument types, and pwetty themes for the most sugoi user expewience! (✿◠‿◠)

## ❀ Instawwation ❀

To instaww **Nyxie-Wixie**, wun this wittle command:

```bash
pip install nyx-cli
```

## (づ￣ ³￣)づ Tabwe of Contents

- [❀ Instawwation ❀](#-instawwation-)
- [✧･ﾟ Examples ･ﾟ✧](#-examples-)
  - [Basic Usage uwu](#basic-usage-uwu)
  - [Custom Wogging](#custom-wogging)
  - [Intewactive Mode (◕ᴗ◕✿)](#intewactive-mode-)
  - [Custom ASCII Awt](#custom-ascii-awt)
- [★彡 Featuwes 彡★](#-featuwes-)
- [✿ Documentation ✿](#-documentation-)
- [(ﾉ◕ヮ◕)ﾉ*:･ﾟ✧ Contwibuting](#-contwibuting)
- [Wicense UwU](#wicense-uwu)

## ✧･ﾟ Examples ･ﾟ✧

### Basic Usage uwu

To use **Nyxie-Wixie**, fiwst impowt it wike dis:

```python
from nyx.nyx import Nyx

# Cweate a Nyx instance (so kawaiiiii)
nyx = Nyx()

nyx.add_arg(
    long="exampwe",
    short="e",
    description="Custom exampwe message desu~",
    required=True,  # Dis makes it mandatowy uwu
    arg_type="str",  # Optional: Define expected type-chan
)

# Configure Nyx (Shows up in hewp `-h` or `--hewp`)
nyx.config(
    description="Dis is a test toow (◕‿◕✿)",
    example_input="--exampwe 'hewwo mummy~!'",
)

# Pawse command-wine awguments
nyx.parse_args()

# Access awgument vawues as object attwiboots!
print(nyx.exampwe)
```

### Custom Wogging

Nyxie-Wixie has super kawaii functions for stwuctuwd and cowor-coded wogging:

```python
nyx = Nyx()
nyx.config(theme="defauwt")  # Defauwt theme if not expwicitwy set uwu

nyx.success("Hewwo wowld", color_text=False)  # Default: Gween
nyx.error("Something bad happened (｡•́︿•̀｡)")  # Wed
nyx.warning("Watch owt senpai!")  # Yewwow
nyx.info("Wandom infowmation OwO")  # Bwue
```

#### Output:

```zsh
  [✔] SUCCESS: Hewwo wowld
  [✖] ERROR: Something bad happened (｡•́︿•̀｡)
  [!] WARNING: Watch owt senpai!
  [*] INFO: Wandom infowmation OwO
```

### Intewactive Mode (◕ᴗ◕✿)

Nyxie-Wixie has a supew kawaii intewactive mode that asks usews for awguments:

```python
nyx = Nyx()

nyx.add_arg(
    long="website",
    short="w",
    description="Website UWL pwease?",
    required=True,
    arg_type="url",
)

nyx.interactive()  # Pwompts usew-chan for input
```

Optionaw awguments will be type checked if they wewen't empty! So smart desu ne~!

You can awso customize the input symbow and its cowor:

```python
nyx.interactive(symbol="♡", color="pink")  # Avaiwable cowors: wed, gween, bwue, yewwow (defauwt: white)
```

### Custom ASCII Awt

If you want to dispway ASCII awt befowe pwogwam execution, Nyxie-Wixie awwows you to set a stawtup function:

```python
def print_ascii():
    print("""
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⣀⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⣀⡴⠞⠛⠉⠉⠉⠉⠉⠛⠶⣄⡀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⢀⡾⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢷⡀⠀⠀⠀⠀
    ⠀⠀⠀⢠⡟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢿⡄⠀⠀⠀
    ⠀⠀⢀⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⡀⠀⠀
    ⠀⠀⣼⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣧⠀⠀
    ⠀⠀⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⡀⠀  NYX-CHAN
    ⠀⠀⣿⡄⠀⠀⠀⣠⣤⣤⣤⣤⣤⣤⣤⣤⣄⡀⠀⠀⠀⢠⣿⠁⠀
    ⠀⠀⠹⣧⠀⠀⠀⠙⣿⣿⣿⣿⣿⣿⣿⡿⠋⠀⠀⠀⣠⡾⠃⠀⠀
    ⠀⠀⠀⠘⢷⣄⠀⠀⠀⠉⠛⠛⠛⠛⠉⠀⠀⠀⣠⡾⠋⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠙⠷⣦⣄⡀⠀⠀⠀⠀⢀⣠⣴⠾⠋⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⠉⠛⠷⠶⠶⠾⠛⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀
    """)

# Two ways to set a stawtup function:
nyx = Nyx(starting_function=print_ascii)  # Option 1
nyx.init(print_ascii)  # Option 2 (≧◡≦)
```

## Awgument Handwing

Nyxie-Wixie hewps usews by weminding them if they miss a wequired awgument. If an awgument is mandatowy and not pwovided, Nyxie-Wixie will dispway an ewwor message indicating which awgument was missing. For exampwe:

```zsh
Ewwor (╥﹏╥): Awgument '--website' wequires a vawue but none was pwovided.
```

Exampwe impwementation:

```python
nyx.add_arg(
    long="website",
    short="w",
    description="Website UWL pwease?",
    required=True,
    arg_type="url",
)

nyx.parse_args()
```

## ★彡 Featuwes 彡★

- **Zewo dependency**: No extewnaw dependencies wequired! So independent desu~
- **Minimaw boiwerpwate**: Easy-to-use API for wapid devewopment (quick wike a ninja~)
- **Custom awgument types**: Suppowts vawidation of awgument types (so smawt!)
- **Intewactive mode**: Automaticawwy pwompts for wequired awguments (´｡• ᵕ •｡`)
- **Theming suppowt**: Customizabwe wogging themes (makes evewything pwetty!)
- **Cowowized output**: Enabwes cweaw and stwuctuwd CLI feedback (rainbows evewywhere~)

## ✿ Documentation ✿

To view suppowted awgument types and avaiwable themes, use these kawaii commands:

```python
nyx.get_types()  # Shows all the types-chan!
nyx.get_themes()  # Shows all the pwetty themes!
```

## (ﾉ◕ヮ◕)ﾉ*:･ﾟ✧ Contwibuting

We wewcome contwibutions! To contwibute, fowwow these steps:
1. Fowk the wepositori (≧◡≦)
2. Cweate a new bwanch (`git checkout -b feature-branch-chan`)
3. Commit youw changes (`git commit -m "Add new sugoi feature"`)
4. Push to the bwanch (`git push origin feature-branch-chan`)
5. Open a Puww Wequest and wait for sempai to notice you!

Pwease make suwe your code fowwows best pwactices and incwudes documentation where necessawy.

## Wicense UwU

**Nyxie-Wixie** is weweased under the The Cuddwy Purrmission License  Wicense. See the [WICENSE](LICENSE) fiwe for detaiws.

## Notes (｡•́︿•̀｡)

- **Awgument Type Handwing**: When using `arg_type` wike `int`, `fwoat`, etc., Nyxie-Wixie vawidates the input but wetuwns it as a stwing. You must convewt it back to the expected type.
- **Async Suppowt**: The `run_async` method is currentwy bwoken (so sadge). Avoid using it in pwoduction.

**Happy hacking with huggins, nya~!** (｡♥‿♥｡)ฅ^•ﻌ•^ฅ
