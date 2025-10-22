## Python practice

### Projects

| Project                    | Description                  |
| :------------------------- | :--------------------------- |
| [Simple App](./SimpleApp)  | Simple API written by Sanic  |
| [Blockchain](./Blockchain) | Blockchain practice          |
| [tutorial](./tutorial/)    | My study                     |
| [game](./games/)           | I try to implement caro game |

### Convert to wasm

##### Step 1:

```shell
git clone https://github.com/emscripten-core/emsdk.git
cd emsdk
```

##### Step 2:

```shell
./emsdk install latest
./emsdk activate latest
```

##### Step 3:

```shell
source ./emsdk_env.sh
```

##### Step 4:

```shell
emcc -v
```
